import string
import time
import math
import torch
from torch.autograd import Variable

all_characters = string.printable
n_characters = len(all_characters)

def read_file(filename):
    """Read input data"""
    data = open(filename).read().split()
    chars = list(set(data))
    data_size, vocab_size = len(data), len(chars)

    print('data has %d vocabs, %d unique.' % (data_size, vocab_size))

    return data, data_size

def char_tensor(s):
    """Convert an input string to tensor"""
    tensor = torch.zeros(len(s)).long()
    for c in range(len(s)):
        tensor[c] = all_characters.index(s[c])
    return Variable(tensor)

def time_since(since):
    """Measure time elapsed"""
    s = time.time() - since
    m = math.floor(s/60)
    s -= m * 60
    return '%dm %ds' % (m, s)