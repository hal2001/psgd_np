"""the RNN add problem; check 'Long short-term memory' for details
"""
import numpy as np
import torch
from torch.autograd import Variable

np.random.seed(0)

# parameter settings
batch_size, seq_len0 = 128, 30
dim_in, dim_out = 2, 1
dim_hidden = 20


# generate training data for the add problem
def get_batches( ):
    seq_len = round(seq_len0 + 0.1*np.random.rand()*seq_len0)
    x = np.zeros([batch_size, seq_len, dim_in])
    y = np.zeros([batch_size, dim_out])
    for i in range(batch_size):
        x[i,:,0] = 2.0*np.random.rand(seq_len) - 1.0
        while True:
            i1, i2 = list(np.floor(np.random.rand(2)*seq_len/2).astype(int))
            if i1 != i2:
                break
        x[i, i1, 1] = 1.0
        x[i, i2, 1] = 1.0
        y[i] = 0.5*(x[i,i1,0] + x[i,i2,0])
    # tranpose x to dimensions: sequence_length * batch_size * dimension_input  
    return np.transpose(x, [1,0,2]), y


# generate a random orthogonal matrix for recurrent matrix initialization 
def get_rand_orth( dim ):
    temp = np.random.normal(size=[dim, dim])
    q, _ = np.linalg.qr(temp)
    return q


# return loss of a vanilla RNN model with parameters=(W1, W2) and inputs=(x, y)
def train_criterion(Ws, x, y):
    W1, W2 = Ws
    ones = Variable(torch.ones(batch_size, 1))

    h = Variable(torch.zeros(batch_size, dim_hidden))
    for xt in x:
        net_in = Variable(torch.FloatTensor(xt))
        h = torch.tanh( torch.cat((net_in, h, ones), dim=1).mm(W1) )
        
    net_out = torch.cat((h, ones), dim=1).mm(W2)
    mse = ((net_out - Variable(torch.FloatTensor(y)))**2).mean()
    # return mean square error
    return mse


# initialize the RNN weights
W1_np = np.concatenate((np.random.normal(loc=0.0, scale=0.1, size=[dim_in, dim_hidden]),
                        get_rand_orth(dim_hidden),
                        np.zeros([1, dim_hidden])), axis=0)
W2_np = np.concatenate((np.random.normal(loc=0.0, scale=0.1, size=[dim_hidden, dim_out]),
                        np.zeros([1, dim_out])), axis=0)
W1 = Variable(torch.FloatTensor(W1_np), requires_grad=True)
W2 = Variable(torch.FloatTensor(W2_np), requires_grad=True)
Ws = [W1, W2]