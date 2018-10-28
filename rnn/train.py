import torch
import torch.nn as nn
import argparse
import random
import os

from utils import *
from model import *
from generate import *

# hyperparameters
filename = "../data/oscar_wilde_lines.txt"
hidden_size = 100
sq_len = 100
lr = 1e-1
n_layers = 2
n_epochs = 2000
print_every = 100 # print training stats every 100 epochs

file, file_len = read_file(filename)

def random_training_set(chunk_len):
    """generate random training sets"""
    start_id = random.randint(0, file_len - chunk_len)
    end_id = start_id + chunk_len + 1
    chunk = file[start_id:end_id]
    inp = char_tensor(chunk[:-1])
    target = char_tensor(chunk[1:])
    return inp, target

# Neural net set-up
decoder = RNN(n_characters, hidden_size, n_characters, n_layers)
decoder_optimizer = torch.optim.Adam(decoder.parameters(), lr=lr)
loss = nn.CrossEntropyLoss()

start = time.time()
all_losses = []
loss_avg = 0

def train(inp, target):
    """Train Torch model"""
    hidden = decoder.init_hidden()

    # zero the gradients before running the backward pass
    decoder.zero_grad()
    l = 0

    for c in range(sq_len):
        output, hidden = decoder(inp[c], hidden)
        l += loss(output, target[c].unsqueeze(0))

    # computes dl/dx for every parameter x that has requires_grad=True
    l.backward()

    # performs a single optimization step
    decoder_optimizer.step()

    return l.data.item()/sq_len

def save():
    """Save trained Torch model"""
    save_fn = os.path.splitext(os.path.basename(filename))[0] + '.pt'
    torch.save(decoder, save_fn)
    print("Saved as %s" % save_fn)

try:
    print("Training for %d epoches..." % n_epochs)
    for epoch in range(1, n_epochs+1):
        l = train(*random_training_set(sq_len))
        loss_avg += l

        if epoch % print_every == 0:
            print("[%s (%d %d%%) %.4f]" % (time_since(start), epoch, epoch / n_epochs * 100, l))
            print(generate(decoder, 'Wh', 100), '\n')

        # print("Saving...")
        save()

except KeyboardInterrupt:
    print("Saving before quitting...")
    save()