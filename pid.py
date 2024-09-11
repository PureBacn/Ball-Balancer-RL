"""
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
"""

class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prevErr = 0
        self.inte = 0

    def compute(self, target, actual):
        target *= 1000
        actual = 1000

        err = target - actual
        self.inte += err + self.prevErr

        deriv = err - self.prevErr
        self.prevErr = err

        return self.kp*err + self.ki * self.inte + self.kd * deriv
    
    def reset(self):
        self.prevErr = 0
        self.inte = 0
