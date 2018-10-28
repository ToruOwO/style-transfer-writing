import torch

from utils import *
from model import *

def generate(decoder, seed_str='A', predict_len=100, temperature=0.8):
    """Generate text using trained model"""

    hidden = decoder.init_hidden()
    seed_input = char_tensor(seed_str)
    predicted = seed_str

    # Use seed to build up hidden state
    for p in range(len(seed_str)-1):
        _, hidden = decoder(seed_input[p], hidden)

    inp = seed_input[-1]

    for p in range(predict_len):
        output, hidden = decoder(inp, hidden)

        # Sample from the network
        output_dist = output.data.view(-1).div(temperature).exp()

        # returns a tensor where each row contains 1 index sampled
        # from the multinomial probability distribution in the
        # row of tensor input
        top_i = torch.multinomial(output_dist, 1)[0]

        # add predicted character to result string and use as next input
        predicted_char = all_characters[top_i]
        predicted += predicted_char
        inp = char_tensor(predicted_char)

    return predicted

if __name__ == '__main__':
    # parse command line arguments
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument('filename', type=str)
    argparser.add_argument('-p', '--seed_str', type=str, default='A')
    argparser.add_argument('-l', '--predict_len', type=int, default=100)
    argparser.add_argument('-t', '--temperature', type=float, default=0.8)
    args = argparser.parse_args()

    decoder = torch.load(args.filename)
    del args.filename
    print(generate(decoder, **vars(args)))