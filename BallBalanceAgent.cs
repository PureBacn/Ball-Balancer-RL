using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Actuators;
using Unity.MLAgents.Sensors;
using UnityEngine.UIElements;
using Unity.VisualScripting;


public class PID
{
	private float _kp, _ki, _kd;
	private float _previousError;
	private float _integral;

	public PID(float kp, float ki, float kd)
	{
		_kp = kp;
		_ki = ki;
		_kd = kd;
		_previousError = 0;
		_integral = 0;
	}

	public float Compute(float setpoint, float actualValue)
	{
		setpoint *= 1000;
		actualValue *= 1000;

		float error = setpoint - actualValue;

		_integral += error + _previousError;

		float derivative = error - _previousError;
		//derivative = float.IsNaN(derivative) || float.IsInfinity(derivative) ? 0 : derivative;
		_previousError = error;

		return _kp * error + _ki * _integral + _kd * derivative;
	}

	public void Reset()
	{
		_previousError = 0;
		_integral = 0;
	}
}

public class Machine
{
	private float d, e, f, g;
	private float nmag, nz;
	private float x, y, z;
	private float mag;
	private float angle;

	public Machine(float kd, float ke, float kf, float kg)
	{
		d = kd;
		e = ke;
		f = kf;
		g = kg;
	}

	public float Compute(int leg, float hz, float nx, float ny)
	{
		//create unit normal vector
		nmag = Mathf.Sqrt(Mathf.Pow(nx, 2) + Mathf.Pow(ny, 2) + 1);  //magnitude of the normal vector
		nx /= nmag;
		ny /= nmag;
		nz = 1 / nmag;
		//calculates angle A, B, or C
		switch (leg)
		{
			case 0:  //Leg A
				y = d + (e / 2) * (1 - (Mathf.Pow(nx, 2) + 3 * Mathf.Pow(nz, 2) + 3 * nz) / (nz + 1 - Mathf.Pow(nx, 2) + (Mathf.Pow(nx, 4) - 3 * Mathf.Pow(nx, 2) * Mathf.Pow(ny, 2)) / ((nz + 1) * (nz + 1 - Mathf.Pow(nx, 2)))));
				z = hz + e * ny;
				mag = Mathf.Sqrt(Mathf.Pow(y, 2) + Mathf.Pow(z, 2));
				angle = Mathf.Acos(y / mag) + Mathf.Acos((Mathf.Pow(mag, 2) + Mathf.Pow(f, 2) - Mathf.Pow(g, 2)) / (2 * mag * f));
				break;
			case 1:  //Leg B
				x = (Mathf.Sqrt(3) / 2) * (e * (1 - (Mathf.Pow(nx, 2) + Mathf.Sqrt(3) * nx * ny) / (nz + 1)) - d);
				y = x / Mathf.Sqrt(3);
				z = hz - (e / 2) * (Mathf.Sqrt(3) * nx + ny);
				mag = Mathf.Sqrt(Mathf.Pow(x, 2) + Mathf.Pow(y, 2) + Mathf.Pow(z, 2));
				angle = Mathf.Acos((Mathf.Sqrt(3) * x + y) / (-2 * mag)) + Mathf.Acos((Mathf.Pow(mag, 2) + Mathf.Pow(f, 2) - Mathf.Pow(g, 2)) / (2 * mag * f));
				break;
			case 2:  //Leg C
				x = (Mathf.Sqrt(3) / 2) * (d - e * (1 - (Mathf.Pow(nx, 2) - Mathf.Sqrt(3) * nx * ny) / (nz + 1)));
				y = -x / Mathf.Sqrt(3);
				z = hz + (e / 2) * (Mathf.Sqrt(3) * nx - ny);
				mag = Mathf.Sqrt(Mathf.Pow(x, 2) + Mathf.Pow(y, 2) + Mathf.Pow(z, 2));
				angle = Mathf.Acos((Mathf.Sqrt(3) * x - y) / (2 * mag)) + Mathf.Acos((Mathf.Pow(mag, 2) + Mathf.Pow(f, 2) - Mathf.Pow(g, 2)) / (2 * mag * f));
				break;
		}
		return (angle * (180 / Mathf.PI));  //converts angle to degrees and returns the value
	}
}

public class BallBalanceAgent : Agent
{
	public GameObject ball;
	public GameObject a1;
	public GameObject a2;
	public GameObject a3;
	public Vector3 start;
	public GameObject platform;
	public Vector2 target;
	public PID pidX = new PID(4E-4f, 2E-6f, 7E-3f);
	public PID pidY = new PID(4E-4f, 2E-6f, 7E-3f);
	public Machine machine = new Machine(2f, 3.125f, 1.75f, 3.669291339f);
	public float score = 0f;

	public float GetAngle(GameObject axle)
	{
		ArticulationBody joint = axle.GetComponent<ArticulationBody>();
		ArticulationDrive drive = joint.xDrive;
		float angle = drive.target;
		return angle;
	}

	public void ShiftAngle(GameObject axle, float angle)
	{
		float per = (angle + 1) / 2;
		ArticulationBody joint = axle.GetComponent<ArticulationBody>();
		ArticulationDrive drive = joint.xDrive;
		float target = drive.lowerLimit + per * (drive.upperLimit - drive.lowerLimit);
		//float target = Mathf.Clamp(drive.target - angle, drive.lowerLimit, drive.upperLimit);
		joint.SetDriveTarget(ArticulationDriveAxis.X, target);
	}

	public void ResetAxle(GameObject axle)
	{
		ArticulationBody joint = axle.GetComponent<ArticulationBody>();
		joint.SetDriveTarget(ArticulationDriveAxis.X, 0);
	}

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
		if (Physics.Raycast(ray, out RaycastHit hit))
		{
			Vector3 hitPos = hit.point;
			return GetRelative(hitPos);
		}
		return new Vector2(-1, -1);
	}

	public float Offset(float angle)
	{
		return angle - 180;
	}

	/*
	public override void Heuristic(in ActionBuffers actionsOut)
	{
		ActionSegment<float> actionSegment = actionsOut.ContinuousActions;

		Vector2 pos = GetBallPos();

		if (pos.x < 0 || pos.y < 0) { return; }

		float outX = -pidX.Compute(0.5f, pos.x);
		float outY = -pidY.Compute(0.5f, pos.y);

		
		//Debug.Log(outX);
		//Debug.Log(outY);
		//platform2.transform.rotation = Quaternion.Euler(-Mathf.Rad2Deg * outX, 0, -Mathf.Rad2Deg * outY);

		float a1 = machine.Compute(0, 4.25f, outX, outY);
		float a2 = machine.Compute(1, 4.25f, outX, outY);
		float a3 = machine.Compute(2, 4.25f, outX, outY);

		actionSegment[1] = (Offset(a1) + 40) / 50;
		actionSegment[0] = (Offset(a2) + 40) / 50;
		actionSegment[2] = (Offset(a3) + 40) / 50;
	}
	*/

	public override void OnEpisodeBegin()
	{
		score = 0;
		pidX.Reset();
		pidY.Reset();
		ResetAxle(a1);
		ResetAxle(a2);
		ResetAxle(a3);

		ball.transform.localPosition = start;
		Rigidbody rigidbody = ball.GetComponent<Rigidbody>();
		//rigidbody.velocity = Vector3.zero;
		rigidbody.velocity = new Vector3((Random.value-0.5f)*2,(Random.value - 0.5f) * 2,(Random.value - 0.5f) * 2);
	}

	public override void CollectObservations(VectorSensor sensor)
	{
		sensor.AddObservation(GetAngle(a1));
		sensor.AddObservation(GetAngle(a2));
		sensor.AddObservation(GetAngle(a3));

		Vector2 pos = GetBallPos();
		sensor.AddObservation(pos);
		sensor.AddObservation(target);
	}

	public override void OnActionReceived(ActionBuffers actions)
	{
		ActionSegment<float> cactions = actions.ContinuousActions;
		ShiftAngle(a1, cactions[0]);
		ShiftAngle(a2, cactions[1]);
		ShiftAngle(a3, cactions[2]);

		/*
		Ray ray = new Ray(ball.transform.position, Vector3.down);
		if (Physics.Raycast(ray, out RaycastHit hit))
		{
			if (ball.transform.position.y - hit.point.y > 2)
			{
				SetReward(-1f);
				EndEpisode();
			}

			SetReward(0.1f);
		}
		else
		{
			SetReward(-1f);
			EndEpisode();
			Debug.Log("Ending...");
		}
		*/

		Vector2 pos = GetBallPos();
		if (pos.x < 0 || pos.y < 0 || ball.transform.localPosition.y > 5) {
			SetReward(-1f);
			score -= 1f;
			EndEpisode();
		}

		float outX = -pidX.Compute(0.5f, pos.x);
		float outY = -pidY.Compute(0.5f, pos.y);

		float an1 = machine.Compute(1, 4.25f, outX, outY);
		float an2 = machine.Compute(0, 4.25f, outX, outY);
		float an3 = machine.Compute(2, 4.25f, outX, outY);

		float g1 = (Offset(an1) + 40) / 50;
		float g2 = (Offset(an2) + 40) / 50;
		float g3 = (Offset(an3) + 40) / 50;

		if (Mathf.Abs(g1 - cactions[0]) <= 0.1 && Mathf.Abs(g2 - cactions[1]) <= 0.1 && Mathf.Abs(g3 - cactions[2]) <= 0.1)
		{
			SetReward(0.25f);
			score += 0.25f;
		}
		else {
			SetReward(-0.05f);
			score -= 0.05f;
		}
	}
}
