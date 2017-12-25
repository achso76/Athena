import numpy as np
import os, sys, inspect

import matplotlib.pyplot as plt

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir) 

from Aspecter import Aspecter

parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir) 

from src.frontend.Box import CommonModuleBox

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable

class Box(CommonModuleBox):
    def __init__(self, parent=None, instName = ''):
        self.typeName = type(self)
        super().__init__(parent, 3, 2, instName, self.typeName)

        self.piTrainingData = self.inPorts[0]
        self.piTrainingData.setPortType(torch.utils.data.dataloader.DataLoader)
        self.piTestData = self.inPorts[1]
        self.piTestData.setPortType(torch.utils.data.dataloader.DataLoader)
        self.piModel = self.inPorts[2]
        self.piModel.setPortType(nn.Module)

    def createPopupActions(self):
        """ createPopupActions method defines popup menu and method when a popup menu is selected by users. 
        """
        menus = [{"title":"Export", "desc":"Export logic to source code", "method":self.export},
                 {"title":"Train", "desc":"Train", "method":self.train},
                 {"title":"Config", "desc":"Configure module parameters", "method":self.config},
                 {"title":"Run", "desc":"Configure module parameters", "method":self.run}]
        self.setPopupActionList(menus)

    def export(self):
        pass

    def train(self):
        pass

    def config(self):
        pass

    def execute(self):

        training_data = self.piTrainingData.getData()
        model = self.piModel.getData()

        for p in model.parameters():
            print(p.size())

        optimizer = optim.Adam(model.parameters(), lr=0.0001)
        batch_size = 50
        model.train()
        train_loss = []
        train_accu = []
        i = 0
        for epoch in range(1):
            for data, target in training_data:
                data, target = Variable(data), Variable(target)
                optimizer.zero_grad()
                output = model(data)
                loss = F.nll_loss(output, target)
                loss.backward()    # calc gradients
                train_loss.append(loss.data[0])
                optimizer.step()   # update gradients
                prediction = output.data.max(1)[1]   # first column has actual prob.
                accuracy = prediction.eq(target.data).sum()/batch_size*100
                train_accu.append(accuracy)
                if i % 10 == 0:
                    print('Train Step: {}\tLoss: {:.3f}\tAccuracy: {:.3f}'.format(i, loss.data[0], accuracy))
                i += 1

        plt.plot(np.arange(len(train_loss)), train_loss)
        plt.plot(np.arange(len(train_accu)), train_accu)

        """
        model.eval()
        correct = 0
        for data, target in test_loader:
            data, target = Variable(data, volatile=True), Variable(target)
            output = model(data)
            prediction = output.data.max(1)[1]
            correct += prediction.eq(target.data).sum()

        print('\nTest set: Accuracy: {:.2f}%'.format(100. * correct / len(test_loader.dataset)))

        self.data = np.random.rand(self.dim[0],self.dim[1])
        
        for port in self.outPorts:
            port.transferData(self.data)
        """
