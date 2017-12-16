# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch
from torch.autograd import Variable
import torch.optim as optim
import numpy as np


from six.moves import cPickle

import opts
import models
import torch.nn as nn
import utils
import torch.nn.functional as F
from torchtext import data
from torchtext import datasets
from torchtext.vocab import Vectors, GloVe, CharNGram, FastText
from torch.nn.modules.loss import NLLLoss,MultiLabelSoftMarginLoss,MultiLabelMarginLoss,BCELoss
import os

if "CUDA_VISIBLE_DEVICES" not in os.environ.keys():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
opt = opts.parse_opt()
opt.model ='lstm'
opt.model ='baisc_cnn'

train_iter, test_iter = utils.loadData(opt)

model=models.setup(opt)
if torch.cuda.is_available():
    model.cuda()
model.train()
optimizer = optim.Adam(model.parameters(), lr=opt.learning_rate)
optimizer.zero_grad()
loss_fun = BCELoss()

#batch = next(iter(train_iter))
#print(utils.evaluation(model,test_iter))
for index,batch in enumerate(train_iter):

    predicted = model(batch.text[0])

    loss= F.cross_entropy(predicted,batch.label)
#    y_onehot = torch.from_numpy(y_onehot)
#    y_onehot = torch.FloatTensor(predicted.size())
#    y_onehot.zero_()
#    ones=torch.ones(batch.label.size())
#    y_onehot.scatter_(1, batch.label.data, 1)
#    loss = loss_fun(predicted,batch.label)
    loss.backward()
    utils.clip_gradient(optimizer, opt.grad_clip)
    optimizer.step()
    if index% 32==0:
        if  torch.cuda.is_available():
            print("loss : %.5f" % loss.cpu().data.numpy()[0])
        else:
            print("loss : %.5f" % loss.data.numpy()[0])

print(utils.evaluation(model,test_iter))


        














    
    







