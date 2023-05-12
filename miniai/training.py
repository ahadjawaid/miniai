# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01-minibatch-training.ipynb.

# %% auto 0
__all__ = ['accuracy', 'report', 'Dataset', 'fit', 'get_dls']

# %% ../nbs/01-minibatch-training.ipynb 1
import pickle,gzip,math,os,time,shutil,torch,matplotlib as mpl,numpy as np,matplotlib.pyplot as plt
from pathlib import Path
from torch import tensor,nn
import torch.nn.functional as F

# %% ../nbs/01-minibatch-training.ipynb 2
def accuracy(preds, targets): return (preds.argmax(1) == targets).float().mean()

# %% ../nbs/01-minibatch-training.ipynb 3
def report(loss, preds, targets): print(f"Loss: {loss:.2f}, Accuracy: {accuracy(preds, targets):.2f}")

# %% ../nbs/01-minibatch-training.ipynb 4
class Dataset:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __len__(self):
        return len(self.x)
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

# %% ../nbs/01-minibatch-training.ipynb 5
from torch.utils.data import DataLoader, SequentialSampler, RandomSampler, BatchSampler

# %% ../nbs/01-minibatch-training.ipynb 6
def fit(epochs, model, loss_func, opt, train_dl, valid_dl):
    for epoch in range(epochs):
        model.train()
        for xb, yb in train_dl:
            preds = model(xb)
            loss = loss_func(preds, yb)
            loss.backward()
            opt.step()
            opt.zero_grad()
        
        model.eval()
        with torch.no_grad():
            tot_loss, tot_acc, count = 0., 0., 0
            for xb, yb in valid_dl:
                preds = model(xb)
                n = len(xb)
                count += n
                tot_loss = loss_func(preds, yb).item() * n
                tot_acc = accuracy(preds, yb).item() * n
        print(epoch, tot_loss/count, tot_acc/count)
    return tot_loss/count, tot_acc/count

# %% ../nbs/01-minibatch-training.ipynb 7
def get_dls(train_ds, valid_ds, bs, **kwargs):
    return (DataLoader(train_ds, bs, shuffle=True, **kwargs),
            DataLoader(valid_ds, bs*2, **kwargs))