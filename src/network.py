"""
network.py
~~~~~~~~~~

This is the file containing the neural network.
"""

# Libraries
### Third-party imports
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import matplotlib.pyplot as plt

import pandas as pd

EPOCH = 0
BATCH_SIZE = 64
LEARNING_RATE = 0.01
NUM_EPOCHS = 16000

RESUME_TRAINING = True


inputs = ((pd.read_csv('inputs.csv')).to_numpy() / 10).astype('float')
answers = pd.read_csv('outputs.csv').to_numpy().astype(int)


def one_hots_from_data(answers):
    """
    Take answers and return one_hot vector.
    This is achieved by slicing long arrays of indices along 
    each axis of a zero-initialized vector, as seen below.
    """
    data_size, input_size = answers.shape 
    y_hat = np.zeros((data_size, input_size, 9))

    slice0 = np.repeat(np.arange(data_size), input_size)
    slice1 = np.tile(np.arange(input_size), data_size)
    sliceOH = answers[slice0, slice1].astype('int8') - 1

    y_hat[slice0, slice1, sliceOH] = 1.
    return y_hat.astype('float')

y_hat = one_hots_from_data(answers)


dataset = TensorDataset(torch.tensor(inputs).float(), torch.tensor(y_hat).float())
train_loader = DataLoader(dataset=dataset, batch_size=BATCH_SIZE, shuffle=True)


class DistributedSoftmax(nn.Module):

    def __init__(self, shape, dim=-1):
        super(DistributedSoftmax, self).__init__()
        self.shape = shape
        self.dim = dim
    
    def forward(self, x):
        batch_size  = x.size()[0]
        rows, columns, indices = self.shape     # will be 9, 9, 9
        input_tensor = x.view(batch_size * rows * columns, indices)
        out = nn.Softmax(dim=self.dim)(input_tensor)
        return out.contiguous().view(batch_size, rows * columns, indices)    # shape = (m, 9, 9, 9)


class DokuNet(nn.Module):

    def __init__(self):
        super(DokuNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(81, 120),
            nn.Tanh(),
            nn.Linear(120, 120),
            nn.ReLU(),
            nn.Linear(120, 120),
            nn.ReLU(),
            nn.Linear(120, 729),
            DistributedSoftmax((9, 9, 9))
        )
    
    def forward(self, x):
        return self.net(x)


model = DokuNet()
optimizer = torch.optim.SGD(
        model.parameters(), lr=LEARNING_RATE, momentum=0.9)

if RESUME_TRAINING:
    checkpoint = torch.load('./history/model64_4000:8000.pt')
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    EPOCH = checkpoint['epoch']

    criterion = nn.BCELoss()


final_cost = None
costs = []

def train():
    for epoch in range(EPOCH, EPOCH+NUM_EPOCHS):
        
        cost = 0

        for batch, targets in train_loader:

            output = model(batch.float())
            loss = criterion(output, targets)
            cost += loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
        print('Epoch [{}/{}], cost: {:.4f}'.format(epoch+1, EPOCH+NUM_EPOCHS, cost))
        costs.append(cost)

        if epoch % 100 == 99:
            plt.plot(range(EPOCH, EPOCH+len(costs)), costs)
            plt.title('Epoch {}, lr={}'.format(epoch + 1, LEARNING_RATE))
            plt.savefig('./cost_plots/{}'.format(epoch+1))

        if epoch == NUM_EPOCHS-1:
            final_cost = costs[-1]
        
        
    torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'cost': final_cost,
            }, './history/model.pt')

if __name__ == '__main__':
    train()