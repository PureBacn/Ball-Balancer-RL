import modelinfo
#from machine import Machine
import numpy as np
import onnxruntime
import os
import time
from serial import Serial


serial = Serial("COM5", baudrate=115200, timeout=0)

modelName = "BallBalancer.2.onnx"
path = f"{os.path.dirname(os.path.abspath(__file__))}\\{modelName}"
sess = onnxruntime.InferenceSession(path)

modelinfo.get(path)
curAngles = (0,0)

start = 0

while True:
    raw = serial.readline()
    data = str(raw)[2:][:-5]
    
    if data.find(" ") == -1 or data[:1] == "!":
        if len(data) > 0:
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

    curAngles = (np.clip(curAngles[0] + x,-0.25,0.25), np.clip(curAngles[1] + z,-0.25,0.25))
    print(f"Angles: {str(curAngles[0])[:20]} {str(curAngles[1])[:20]}\n")

    angles = str.encode(f"{str(curAngles[0])[:20]} {str(curAngles[1])[:20]}\n")
    serial.write(angles)
    print(f"Time: ", time.time()-start)
    start = time.time()


"""
          POV: You Work At Google
⣿⠟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⢻⣿⣿⡇
⣿⡆⠊⠈⣿⢿⡟⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣎⠈⠻⣿⡇
⣿⣷⣠⠁⢀⠰⠀⣰⣿⣿⣿⣿⣿⣿⠟⠋⠛⠛⠿⠿⢿⣿⣿⣿⣧⠀⢹⣿⡑⠐ ⣿⣿
⣿⣿⣿⠀⠁⠀⠀⣿⣿⣿⣿⠟⡩⠐⠀⠀⠀⠀⢐⠠⠈⠊⣿⣿⣿⡇⠘⠁⢀⠆⢀⣿⣿⡇
⣿⣿⣿⣆⠀⠀⢤⣿⣿⡿⠃⠈⠀⣠⣶⣿⣿⣷⣦⡀⠀⠀⠈⢿⣿⣇⡆⠀⠀⣠⣾⣿⣿⡇
⣿⣿⣿⣿⣧⣦⣿⣿⣿⡏⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠐⣿⣿⣷⣦⣷⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⣾⣿⣿⠋⠁⠀⠉⠻⣿⣿⣧⠀⠠⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⡿⠁⠀⠀⠀⠀⠀⠘⢿⣿⠀⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣠⣂⠀⠀⠀⠀⠀⠀⠀⢀⣁⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣄⣤⣤⣔⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
"""