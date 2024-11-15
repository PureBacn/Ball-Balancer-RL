using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using UnityEngine.UIElements;
using Unity.VisualScripting;

public class BallBalanceAgent : Agent
{
	public GameObject ball;
	public Vector3 start;
	public GameObject a1;
	public GameObject a2;
	public GameObject a3;
	public GameObject platform;
	public float yeetFactor;
	public Quaternion startingOrientation;
	public Vector3 currentOrientation;
	public float maxAngle = Mathf.Rad2Deg * 0.25f;

	public Machine machine = new Machine(2f, 3.125f, 1.75f, 3.669291339f);

	public Vector2 GetRelative(Vector3 pos)
	{
		Vector3 size = platform.GetComponent<MeshRenderer>().bounds.size;
		Vector3 corner = platform.transform.position - platform.transform.right * size.x / 2 - platform.transform.forward * size.z / 2;
		Vector3 diagonal = pos - corner;

		float xLen = Vector3.Dot(platform.transform.right, diagonal);
		float zLen = Vector3.Dot(platform.transform.forward, diagonal);

		if (xLen < 0 || zLen < 0)
		{
			return new Vector2(-1, -1);
		}

		return new Vector2(xLen / size.x, zLen / size.z);
	}

	public Vector2 GetBallPos()
	{
		Ray ray = new Ray(ball.transform.position, Vector3.down);
		if (Physics.Raycast(ray, out RaycastHit hit, 100))
		{
			Vector3 hitPos = hit.point;
			return GetRelative(hitPos);
		}
		return new Vector2(-1, -1);
	}

	public void MoveTo(Vector2 angles)
	{
		a1.GetComponent<ArticulationBody>().SetDriveTarget(ArticulationDriveAxis.X,machine.Compute(0, 4.25f, angles[0], angles[1]));
		a2.GetComponent<ArticulationBody>().SetDriveTarget(ArticulationDriveAxis.X,machine.Compute(1, 4.25f, angles[0], angles[1]));
		a3.GetComponent<ArticulationBody>().SetDriveTarget(ArticulationDriveAxis.X,machine.Compute(2, 4.25f, angles[0], angles[1]));
	}

	public override void OnEpisodeBegin()
	{
		MoveTo(new Vector2(0, 0));
		ball.transform.localPosition = start + new Vector3((Random.value - 0.5f) / 10, 0, (Random.value - 0.5f) / 10);
		Rigidbody rigidbody = ball.GetComponent<Rigidbody>();
		//rigidbody.velocity = Vector3.zero;
		rigidbody.velocity = new Vector3((Random.value - 0.5f) * yeetFactor, 0, (Random.value - 0.5f) * yeetFactor);
	}

	public override void CollectObservations(VectorSensor sensor)
	{
		/*
		sensor.AddObservation(-currentOrientation.z);
		sensor.AddObservation(currentOrientation.x);
		*/
		Vector2 pos = GetBallPos();
		sensor.AddObservation(pos);
	}

	public override void OnActionReceived(ActionBuffers actions)
	{
		ActionSegment<float> cactions = actions.ContinuousActions;

		float aX = -cactions[0] * maxAngle;
		float aZ = cactions[1] * maxAngle;

		Debug.Log(new Vector2(aX, aZ));

		MoveTo(new Vector2(aX, aZ));

		Vector2 pos = GetBallPos();
		if (pos.x < 0 || pos.y < 0)
		{
			SetReward(-1f);
			EndEpisode();
		}
		else
		{
			float dist = Mathf.Sqrt(Mathf.Pow(pos.x - 0.5f, 2) + Mathf.Pow(pos.y - 0.5f, 2));
			if (dist < 0.25f)
			{
				SetReward(Mathf.Clamp(Mathf.Abs(dist - 0.25f), 0f, 0.25f));
			}
			else
			{
				SetReward(-0.05f);
			}

			AddReward(0.1f);
		}
	}

	public void Update()
	{
		Rigidbody rigidbody = ball.GetComponent<Rigidbody>();
		if (rigidbody.IsSleeping())
		{
			Debug.Log("Waking Ball");
			rigidbody.WakeUp();
		}
		//Debug.Log(GetBallPos());
	}
}