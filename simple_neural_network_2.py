import numpy as np

class NeuralNetworks():

    def __init__(self):
        np.random.seed(1)

        #3(inputs)x1(output) matrix random values between -1 and 1 with mean 0
        self.synaptic_weights = 2*np.random.random((3,1)) - 1

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def sigmoid_derivative(self, x):
        return x*(1-x)

    def train(self, train_input, train_output, train_iteration):
        for i in range(train_iteration):
            output = self.think(train_input)
            #back propogation
            error = train_output - output
            adjustments = np.dot(\
            train_input.T, error*self.sigmoid_derivative(output))
            self.synaptic_weights += adjustments

    def think(self, input_layer):
        input_layer = input_layer.astype(float)
        output = self.sigmoid(np.dot(input_layer, self.synaptic_weights))
        return output

if __name__ == "__main__":

    neural_network = NeuralNetworks()

    print('Starting synaptic_weights:')
    print(neural_network.synaptic_weights)

    train_input = np.array([[0,0,1],[1,1,1],[1,0,1],[0,1,1]])
    train_output = np.array([[0,1,1,0]]).T #transpose to make it 4x1

    neural_network.train(train_input, train_output, 500)

    print('Synaptic_weights after training:')
    print(neural_network.synaptic_weights)

    #predict new output from what input user provides
    predict = list(map(int, input('Enter test input values: ').split()))
    print('Output data:')
    print(neural_network.think(np.array(predict)))
