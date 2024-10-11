import modelinfo
#from machine import Machine
import numpy as np
import onnxruntime
import os
import time
from serial import Serial


serial = Serial("COM5", baudrate=115200, timeout=0)

modelName = "BallBalancerScaledFINAL.onnx"
path = f"{os.path.dirname(os.path.abspath(__file__))}\\{modelName}"
sess = onnxruntime.InferenceSession(path)

modelinfo.get(path)
#curAngles = (0,0)
limit = np.degrees(0.25)
last = (0,0)
deltInflu = 5
weight = 10
start = 0
x,y = 0,0

def retrieveData():
    return [x,y]


while True:
    raw = serial.readline()
    data = str(raw)[2:][:-5]
    
    if data.find(" ") == -1 or data[:1] == "!":
        if len(data) > 0:
            if data == "!Reset":
                last = (0,0)
                continue
            print("\033[1;32m", end="")
            print(f"Received: {data}")
        continue

    numData = [eval(x) for x in data.split()]
    print("\033[1;34m", end="")
    x, y = numData
    
    #delta = (x-last[0],y-last[1])

    print(f"Point: {x} {y}")
    
    data = np.array([retrieveData()])
    data = data.astype(np.float32)
    result = sess.run(["continuous_actions"],{"obs_0" : data})
    xa, za = result[0].flatten()
    print(f"Angle: {xa*limit} {za*limit}")
    
    angles = str.encode(f"{str(np.radians(xa*limit))[:20]} {str(np.radians(za*limit))[:20]}\n")
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