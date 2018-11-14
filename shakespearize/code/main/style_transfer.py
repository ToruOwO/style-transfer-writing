import tensorflow as tf
# Set seed for reproducability
tf.set_random_seed(1)
import numpy as np
np.random.seed(1)

from keras.preprocessing.sequence import pad_sequences
import configuration as config
import pickle
import sys
import mt_model as models
import utilities as datasets
import utilities
import mt_solver as solver
from prepro import PreProcessing

data_src = config.data_dir

def preprocess(filename):
    unknown_word = "UNK".lower()
    sent_start = "SENTSTART".lower()
    sent_end = "SENTEND".lower()
    pad_word = "PADWORD".lower()
    special_tokens = [sent_start, sent_end, pad_word, unknown_word]

    pp = PreProcessing()
    inp_src = data_src + filename
    inp_data = open(inp_src,"r").readlines()

    # load vocab
    inputs = pp.preprocess(inp_data)
    word_to_idx = pp.word_to_idx
    idx_to_word = pp.idx_to_word
    word_to_idx_ctr = pp.word_to_idx_ctr
    word_counters = pp.word_counters

    texts = inputs
    for t in texts:
        for token in t:
            if token not in word_to_idx:
                word_to_idx[token] = word_to_idx_ctr
                idx_to_word[word_to_idx_ctr] = token
                word_to_idx_ctr += 1
                word_counters[token] = 0
            word_counters[token] += 1

    # generate sequences
    sequences = []
    for t in texts:
        tmp = [word_to_idx[sent_start]]
        for token in t:
            if token not in word_to_idx:
                tmp.append(word_to_idx[unknown_word])
            else:
                tmp.append(word_to_idx[token])
        tmp.append(word_to_idx[sent_end])
        sequences.append(tmp)
    sequences = pad_sequences(sequences,
                              maxlen=config.max_input_seq_length,
                              padding='pre',
                              truncating='post')

    # get encoder and decoder input
    encoder_inputs = np.array(sequences)
    decoder_outputs = np.array(sequences)

    pp.word_to_idx = word_to_idx
    pp.idx_to_word = idx_to_word
    pp.vocab_size = len(word_to_idx)
    pp.word_to_idx_ctr = word_to_idx_ctr
    pp.word_counters = word_counters

    return pp, encoder_inputs, decoder_outputs


def main():
    # params
    params = {}
    params['embeddings_dim'] = config.embeddings_dim
    params['lstm_cell_size'] = config.lstm_cell_size
    params['max_input_seq_length'] = config.max_input_seq_length

    # inputs are all but last element,
    # outputs are all but first element
    params['max_output_seq_length'] = config.max_output_seq_length - 1

    params['batch_size'] = config.batch_size
    params['pretrained_embeddings'] = config.use_pretrained_embeddings
    params['share_encoder_decoder_embeddings'] = config.share_encoder_decoder_embeddings
    params['use_pointer'] = config.use_pointer
    params['pretrained_embeddings_path'] = config.pretrained_embeddings_path
    params['pretrained_embeddings_are_trainable'] = config.pretrained_embeddings_are_trainable
    params['use_additional_info_from_pretrained_embeddings'] = config.use_additional_info_from_pretrained_embeddings
    params['max_vocab_size'] = config.max_vocab_size
    params['do_vocab_pruning'] = config.do_vocab_pruning
    params['use_reverse_encoder'] = config.use_reverse_encoder
    params['use_sentinel_loss'] = config.use_sentinel_loss
    params['lambd'] = config.lambd
    params['use_context_for_out'] = config.use_context_for_out

    print "PARAMS:"
    for key, value in params.items():
        print " -- ", key, " = ", value
    buckets = {0: {'max_input_seq_length': params['max_input_seq_length'],
                   'max_output_seq_length': params['max_output_seq_length']}}

    # Preprocess data
    preprocessing, val_encoder_inputs, val_decoder_outputs = preprocess("style_transfer_test.in")
    params['vocab_size'] = preprocessing.vocab_size

    # Pretrained embeddibngs
    if params['pretrained_embeddings']:
        pretrained_embeddings = pickle.load(open(params['pretrained_embeddings_path'], "r"))
        word_to_idx = preprocessing.word_to_idx
        encoder_embedding_matrix = np.random.rand(params['vocab_size'], params['embeddings_dim'])
        decoder_embedding_matrix = np.random.rand(params['vocab_size'], params['embeddings_dim'])
        not_found_count = 0
        for token, idx in word_to_idx.items():
            if token in pretrained_embeddings:
                encoder_embedding_matrix[idx] = pretrained_embeddings[token]
                decoder_embedding_matrix[idx] = pretrained_embeddings[token]
            else:
                if not_found_count < 10:
                    print "No pretrained embedding for (only first 10 such cases will be printed. other prints are suppressed) ", token
                not_found_count += 1
        print "not found count = ", not_found_count
        params['encoder_embeddings_matrix'] = encoder_embedding_matrix
        params['decoder_embeddings_matrix'] = decoder_embedding_matrix

        if params['use_additional_info_from_pretrained_embeddings']:
            additional_count = 0
            tmp = []
            for token in pretrained_embeddings:
                if token not in preprocessing.word_to_idx:
                    preprocessing.word_to_idx[token] = preprocessing.word_to_idx_ctr
                    preprocessing.idx_to_word[preprocessing.word_to_idx_ctr] = token
                    preprocessing.word_to_idx_ctr += 1
                    tmp.append(pretrained_embeddings[token])
                    additional_count += 1
            print "additional_count = ",additional_count
            params['vocab_size'] = preprocessing.word_to_idx_ctr
            tmp = np.array(tmp)
            encoder_embedding_matrix = np.vstack([encoder_embedding_matrix, tmp])
            decoder_embedding_matrix = np.vstack([decoder_embedding_matrix, tmp])
        print "decoder_embedding_matrix.shape ",decoder_embedding_matrix.shape
        print "New vocab size = ",params['vocab_size']

    # Make inference
    saved_model_path = sys.argv[2]
    print "saved_model_path = ", saved_model_path
    inference_type = "greedy"
    print "inference_type = ", inference_type
    params['saved_model_path'] = saved_model_path
    rnn_model = solver.Solver(params, buckets=None, mode='inference')
    _ = rnn_model.getModel(params, mode='inference', reuse=False, buckets=None)
    print "----Running inference-----"

    # val
    print "val_encoder_inputs = ",val_encoder_inputs
    if len(val_decoder_outputs.shape) == 3:
        val_decoder_outputs = np.reshape(val_decoder_outputs,
                                         (val_decoder_outputs.shape[0], val_decoder_outputs.shape[1]))
    decoder_outputs_inference, decoder_ground_truth_outputs = rnn_model.solveAll(params, val_encoder_inputs,
                                                                                 val_decoder_outputs,
                                                                                 preprocessing.idx_to_word,
                                                                                 inference_type=inference_type)
    validOutFile_name = saved_model_path + ".style_transfer_test.output"
    original_data_path = data_src + "style_transfer_test.in"
    BLEUOutputFile_path = saved_model_path + ".style_transfer_test.BLEU"
    utilities.getBlue(validOutFile_name, original_data_path, BLEUOutputFile_path, decoder_outputs_inference,
                      decoder_ground_truth_outputs, preprocessing)

if __name__ == '__main__':
    main()