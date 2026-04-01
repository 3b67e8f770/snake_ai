#!/usr/bin/python3
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import os


class Linear_QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # 11 input, 3 output
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # learning
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x
    
    def save(self, file_name='model_path'):
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)
        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr  # how fast it's learns
        self.gamma = gamma # HOw important is the present
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr) #values otimizer 
        self.criterion = nn.MSELoss() # mean Squared Error

    def train_step(self, state, action,reward, next_state, done):
        # to tensors
        state = torch.tensor(np.array(state), dtype=torch.float)
        next_state = torch.tensor(np.array(next_state), dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # done? end?

        if len(state.shape) == 1:
            #input checking
            state = torch.unsqueeze(state,0)
            next_state = torch.unsqueeze(next_state,0)
            action = torch.unsqueeze(action,0)
            reward = torch.unsqueeze(reward,0)
            done = (done, )
        #Q = ?
        pred = self.model(state)

        # Bellman's algoritm
        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            
            # action update 
            target[idx][torch.argmax(action[idx]).item()] = Q_new

        # Optymalization
        self.optimizer.zero_grad() # clear
        loss = self.criterion(target, pred) # accuracy
        loss.backward() # the couse of the error
        self.optimizer.step() # update the values
