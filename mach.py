import scipy as sp
import random


controls = ['x', 'left', 'right']
random.seed()


def perceptron(x, weight, bias):
	return 1 if (weight*x + b > 0) else 0

def sigmoid(x):
    return math.tanh(x)

def random_matrix(size, a, b):
    return (b-a) * sp.random.random_sample((size[0], size[1])) + a


class Mach:
	def __init__(self, num_input, num_hidden, num_output):
		#Input, hidden and output nodes
		self.num_input = num_input + 1 #+1 for bias node
		self.num_hidden = num_hidden
		self.num_output = num_output


		#Node activation
		self.input_activation = sp.array(sp.vstack([1.0]*num_input))
		self.hidden_activation = sp.array(sp.vstack([1.0]*num_hidden))
		self.output_activation = sp.array(sp.vstack([1.0]*num_output))


		#Weights
		self.input_hidden_weights = random_matrix((self.num_input, self.num_hidden), -.2, .2)
		self.hidden_output_weights = random_matrix((self.num_hidden, self.num_output), -2, 2)

	def update_nodes(self, inputs):
		if len(inputs) != self.num_input - 1:
			raise ValueError("Incorrect number of inputs!")

		#Inputs
		for i in range(self.num_input - 1):
			self.input_activation[i] = inputs[i] 

		#Hidden
		for j in range(self.num_hidden):
			sum = 0
			for i in range(slef.num_input):
				sum += self.input_activation[i] * self.input_hidden_weights[i][j]
			self.hidden_activation[j] = sigmoid(sum)

		#Outputs
		for k in range(self.num_output):
			sum = 0
			for j in range(self.num_hidden):
				sum += self.hidden_activation[j] * self.hidden_output_weights[j][k]
			self.output_activation[k] = sigmoid(sum)

		return self.output_activation[:]


if __name__ == '__main__':
	m = Mach(4, 2, 3)