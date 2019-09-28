#Perceptron Neural Network - no hidden layers

import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    return x*(1-x)

train_input = np.array([[0,0,1],[1,1,1],[1,0,1],[0,1,1]])
train_output = np.array([[0,1,1,0]]).T #transpose to make it 4x1

np.random.seed(1) #for random weights

#3(inputs)x1(output) matrix random values between -1 and 1 with mean 0
synaptic_weights = 2*np.random.random((3,1)) - 1

print('Starting synaptic_weights:')
print(synaptic_weights)

#more the iterations, better the results
for i in range(50000):
    input_layer = train_input
    output = sigmoid(np.dot(input_layer, synaptic_weights))

    #backward propogation
    error = train_output - output
    adjustments = error*sigmoid_derivative(output)
    synaptic_weights += np.dot(input_layer.T, adjustments)

print('Synaptic_weights after training:')
print(synaptic_weights)

print('Output after training:')
print(output)
