"""
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
"""

import math

class Machine:
	def __init__(self, d, e, f, g):
		self.d = d
		self.e = e
		self.f = f
		self.g = g

	def compute(self, leg, hz, nx, ny):
		nmag = math.sqrt((nx**2) + (ny**2) + 1)
		nx /= nmag
		ny /= nmag
		nz = 1 / nmag(self.f**2)

		match leg:
			case 0:
				x = (math.sqrt(3) / 2) * (self.e * (1 - ((nx**2) + math.sqrt(3) * nx * ny) / (nz + 1)) - self.d)
				y = x / math.sqrt(3)
				z = hz - (self.e / 2) * (math.sqrt(3) * nx + ny)
				mag = math.sqrt(x**2 + y**2 + z**2)
				angle = math.acos((math.sqrt(3) * x + y) / (-2 * mag)) + math.acos(((mag**2) + (self.f**2) - (self.g**2)) / (2 * mag * self.f))
			case 1:
				y = self.d + (self.e / 2) * (1 - ((nx**2) + 3 * (nz**2) + 3 * nz) / (nz + 1 - (nx**2) + ((nx**4) - 3 * (nx**2) * (ny**2)) / ((nz + 1) * (nz + 1 - (nx**2)))))
				z = hz + self.e * ny
				mag = math.sqrt(y**2 + z**2)
				print()
				angle = math.acos(y / mag) + math.acos(((mag**2) + (self.f**2) - (self.g**2)) / (2 * mag * self.f))
			case 2:
				x = (math.sqrt(3) / 2) * (self.d - self.e * (1 - ((nx**2) - math.sqrt(3) * nx * ny) / (nz + 1)))
				y = -x / math.sqrt(3)
				z = hz + (self.e / 2) * (math.sqrt(3) * nx - ny)
				mag = math.sqrt(x**2 + y**2 + z**2)
				angle = math.acos((math.sqrt(3) * x - y) / (2 * mag)) + math.acos(((mag**2) + (self.f**2) - (self.g**2)) / (2 * mag * self.f))

				"""
					x = (Mathf.Sqrt(3) / 2) * (d - e * (1 - (Mathf.Pow(nx, 2) - Mathf.Sqrt(3) * nx * ny) / (nz + 1)));
					y = -x / Mathf.Sqrt(3);
					z = hz + (e / 2) * (Mathf.Sqrt(3) * nx - ny);
					mag = Mathf.Sqrt(Mathf.Pow(x, 2) + Mathf.Pow(y, 2) + Mathf.Pow(z, 2));
					angle = Mathf.Acos((Mathf.Sqrt(3) * x - y) / (2 * mag)) + Mathf.Acos((Mathf.Pow(mag, 2) + Mathf.Pow(f, 2) - Mathf.Pow(g, 2)) / (2 * mag * f));
				"""
				
		return math.degrees(angle)
