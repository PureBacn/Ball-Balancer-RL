import onnxruntime
import onnx
import numpy as np
path = "D:\OneDrive\Desktop\BallBalancer\BallBalance.onnx"
sess = onnxruntime.InferenceSession(path)

model = onnx.load(path)
output =[node.name for node in model.graph.output]

input_all = [node.name for node in model.graph.input]
input_initializer =  [node.name for node in model.graph.initializer]
net_feed_input = list(set(input_all)  - set(input_initializer))

print('Inputs: ', net_feed_input)
print('Outputs: ', output)

for input in model.graph.input:
    print (input.name, end=": ")
    # get type of input tensor
    tensor_type = input.type.tensor_type
    # check if it has a shape:
    if (tensor_type.HasField("shape")):
        # iterate through dimensions of the shape:
        for d in tensor_type.shape.dim:
            # the dimension may have a definite (integer) value or a symbolic identifier or neither:
            if (d.HasField("dim_value")):
                print (d.dim_value, end=", ")  # known dimension
            elif (d.HasField("dim_param")):
                print (d.dim_param, end=", ")  # unknown dimension with symbolic name
            else:
                print ("?", end=", ")  # unknown dimension with no name
    else:
        print ("unknown rank", end="")
    print()


iData = np.array([[1,2,3,4,5]])
iData = iData.astype(np.float32)
result = sess.run(["continuous_actions"],{"obs_0" : iData})
print(result)
x, y, z = result[0].flatten()
print(x,y,z)

"""
#vector_observation:0
x = np.array([[-4.141203 , -0.8933127 , -3.927535 , -1.150026]])
x = x.astype(np.float32)
#action_masks:0
y = np.array([[-1.031152 , -1.114622 , -1.154025]])
y = y.astype(np.float32)
result = sess.run([output_name], {"vector_observation:0": x, "action_masks:0": y})
"""