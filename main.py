import onnxruntime
import numpy as np
import os

import modelinfo

modelName = "BallBalance.onnx"
path = f"{os.path.dirname(os.path.abspath(__file__))}\\{modelName}"
sess = onnxruntime.InferenceSession(path)

modelinfo.get(path)

data = np.array([[1,2,3,4,5]])
data = data.astype(np.float32)
result = sess.run(["continuous_actions"],{"obs_0" : data})
print(result)
x, y, z = result[0].flatten()
print(x,y,z)
