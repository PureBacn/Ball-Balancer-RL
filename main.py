import modelinfo
#from machine import Machine
import numpy as np
import onnxruntime
import os
from serial import Serial

#machine = Machine(2, 3.125, 1.75, 3.669291339)
serial = Serial("COM5", 9600, timeout=1)

modelName = "BallBalancer.2.onnx"
path = f"{os.path.dirname(os.path.abspath(__file__))}\\{modelName}"
sess = onnxruntime.InferenceSession(path)

modelinfo.get(path)
curAngles = (0,0)

while True:
    raw = serial.readline()
    data = str(raw)[2:][:-5]
        
    if data.find(" ") == -1 or data[:1] == "!":
        if data[:1] == "!":
            print("\033[1;32m", end="")
            print(f"Received: {data}")
        continue
    numData = [eval(x) for x in data.split()]
    print("\033[1;34m", end="")
    print(f"Point: {data}")
    x, y = numData

    data = np.array([[curAngles[0],curAngles[1],x,y]])
    data = data.astype(np.float32)
    result = sess.run(["continuous_actions"],{"obs_0" : data})
    x, z = result[0].flatten()
    print(f"Result: {x,z}")

    curAngles = (curAngles[0] + x, curAngles[1] + z)
    print(f"Angles: {curAngles}\n")

    """
    a0 = machine.compute(0, 4.25, curAngles[0], curAngles[1])
    a1 = machine.compute(1, 4.25, curAngles[0], curAngles[1])
    a2 = machine.compute(2, 4.25, curAngles[0], curAngles[1])

    print(a0, a1, a2)

    angles = str.encode(f"{a0} {a1} {a2}")
    serial.write(angles)"""

    angles = str.encode(f"{curAngles[0]} {curAngles[1]}")
    serial.write(angles)