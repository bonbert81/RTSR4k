#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 12:01:22 2020

@author: djoghurt
"""
import argparse
import os
from os import listdir

import numpy as np
import torch
from PIL import Image
from torch.autograd import Variable
from torchvision.transforms import ToTensor
from tqdm import tqdm

from data_utils import is_image_file
from model import Net

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
from torchvision import transforms
from data_utils import DatasetFromFolder
from Jort import Net
import cv2

UPSCALE_FACTOR = 3

trainset = DatasetFromFolder('data/train', upscale_factor=UPSCALE_FACTOR, input_transform=transforms.ToTensor(),
                                  target_transform=transforms.ToTensor())

trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)

" load net "
PATH = 'jortTrained.pth'
net = Net(UPSCALE_FACTOR)
net.load_state_dict(torch.load(PATH))

path = 'data/train/SRF_3/data/'
image_name = '2007_000033.jpg'

img = Image.open(path + image_name).convert('YCbCr')
y, cb, cr = img.split()
image = Variable(ToTensor()(y)).view(1, -1, y.size[1], y.size[0])

inputs, target = next(iter(trainloader))
pic = inputs.numpy()
output = net(inputs)


out = net(image)
out_img_y = out.data[0].numpy()
out_img_y *= 255.0
out_img_y = out_img_y.clip(0, 255)
out_img_y = Image.fromarray(np.uint8(out_img_y[0]), mode='L')
out_img_cb = cb.resize(out_img_y.size, Image.BICUBIC)
out_img_cr = cr.resize(out_img_y.size, Image.BICUBIC)
out_img = Image.merge('YCbCr', [out_img_y, out_img_cb, out_img_cr]).convert('RGB')
out_img.save('test.jpg')
