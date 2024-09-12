import modelinfo
import numpy as np
import onnxruntime
import os
from serial import Serial


serial = Serial("COM3", 9600, timeout=1)

modelName = "BallBalancer.1.onnx"
path = f"{os.path.dirname(os.path.abspath(__file__))}\\{modelName}"
sess = onnxruntime.InferenceSession(path)

modelinfo.get(path)
panelSize = (1000,1000)
curAngles = (0,0)

while True:
    data = str(serial.readline())[2:][:-5]
    
    if data.find(" ") == -1:
        print(data.find(" "))
        continue
    numData = [eval(x) for x in data.split()]
    print(data)
    x, y = numData
    print(x, y)

    data = np.array([[curAngles[0],curAngles[1],x/panelSize[0],y/panelSize[1]]])
    data = data.astype(np.float32)
    result = sess.run(["continuous_actions"],{"obs_0" : data})
    x, z = result[0].flatten()
    curAngles += (x,z)
    print(x,z)
