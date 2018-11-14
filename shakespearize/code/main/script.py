import sys

from load_model_demo import *

def demo(inp):
    return load_model_demo.run_demo(inp)

def tokenize(sentence):
    tokens = []
    token = ''
    for c in sentence:
        if c == '.' or c == ',':
            if tokens != '':
                tokens.append(token)
            token = c
        elif c == ' ':
            if tokens != '':
                tokens.append(token)
            token = ''
        else:
            token += c

    if token != ' ':
        tokens.append(token.lower())

    return tokens + ["sentend"]

if __name__ == '__main__':
    demo = Demo()
    demo.loadModel("./tmp/seq2seq6.ckpt")

    print('Model loaded')
    sys.stdout.flush()

    while True:
        line = sys.stdin.readline()
        # tokens = tokenize(line.strip())

        print(demo.getOutput([line.strip()]))
        sys.stdout.flush()
    # print(demo(['young', 'man', ',', "something's", 'wrong', 'if', "you're", 'getting', 'out', 'of', 'bed', 'this', 'early', '.', 'sentend']))
    # print(demo(['i', 'love', 'you', '.', 'sentend']))