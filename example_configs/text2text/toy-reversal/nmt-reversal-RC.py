# pylint: skip-file
from __future__ import absolute_import, division, print_function
from __future__ import unicode_literals

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

from open_seq2seq.models import Text2Text
from open_seq2seq.encoders import BidirectionalRNNEncoderWithEmbedding
from open_seq2seq.decoders import ConvS2SDecoder

from open_seq2seq.data.text2text.text2text import ParallelTextDataLayer
from open_seq2seq.losses import BasicSequenceLoss

from open_seq2seq.data.text2text.tokenizer import EOS_ID
from open_seq2seq.data.text2text.text2text import SpecialTextTokens
from open_seq2seq.optimizers.lr_policies import fixed_lr

"""
This configuration file describes bidirectional rnn based encoder and convolutional decoder
on the toy task of reversing sequences
"""

base_model = Text2Text
d_model = 128
num_layers = 2

base_params = {
  "use_horovod": False,
  "num_gpus": 1,
  "batch_size_per_gpu": 64,
  "max_steps": 1000,
  "save_summaries_steps": 10,
  "print_loss_steps": 10,
  "print_samples_steps": 20,
  "eval_steps": 50,
  "save_checkpoint_steps": 200,

  "logdir": "ReversalTask-RNN-Conv",

  "optimizer": "Adam",
  "optimizer_params": {"epsilon": 1e-9},
  "lr_policy": fixed_lr,
  "lr_policy_params": {
    'learning_rate': 1e-3
  },

  "max_grad_norm": 3.0,
  "dtype": tf.float32,
  # "dtype": "mixed",
  # "loss_scaling": "Backoff",

  "summaries": ['learning_rate', 'variables', 'gradients', 'larc_summaries',
                'variable_norm', 'gradient_norm', 'global_gradient_norm'],

  "encoder": BidirectionalRNNEncoderWithEmbedding,
  "encoder_params": {
    "core_cell": tf.nn.rnn_cell.LSTMCell,
    "core_cell_params": {
      "num_units": int(d_model/2),
    },

    "encoder_layers": num_layers,
    "encoder_dp_input_keep_prob": 0.8,
    "encoder_dp_output_keep_prob": 1.0,
    "encoder_use_skip_connections": False,
    "src_emb_size": d_model,
  },

  "decoder": ConvS2SDecoder,
  "decoder_params": {
    "shared_embed": True,
    "tgt_emb_size": d_model,

    "conv_nchannels_kwidth": [(d_model, 3)] * num_layers,

    "embedding_dropout_keep_prob": 0.9,
    "hidden_dropout_keep_prob": 0.9,
    "out_dropout_keep_prob": 0.9,

    "max_input_length": 100,
    "extra_decode_length": 10,
    "beam_size": 5,
    "alpha": 0.6,

    "EOS_ID": EOS_ID,
    "GO_SYMBOL": SpecialTextTokens.S_ID.value,
    "END_SYMBOL": SpecialTextTokens.EOS_ID.value,
    "PAD_SYMBOL": SpecialTextTokens.PAD_ID.value,
  },

  "loss": BasicSequenceLoss,
  "loss_params": {
    "offset_target_by_one": True,
    "average_across_timestep": True,
    "do_mask": True
  }
}

train_params = {
  "data_layer": ParallelTextDataLayer,
  "data_layer_params": {
    "src_vocab_file": "toy_text_data/vocab/source.txt",
    "tgt_vocab_file": "toy_text_data/vocab/target.txt",
    "source_file": "toy_text_data/train/source.txt",
    "target_file": "toy_text_data/train/target.txt",
    "shuffle": True,
    "repeat": True,
    "max_length": 56,
    "delimiter": " ",
    "special_tokens_already_in_vocab": False,
  },
}

eval_params = {
  "data_layer": ParallelTextDataLayer,
  "data_layer_params": {
    "src_vocab_file": "toy_text_data/vocab/source.txt",
    "tgt_vocab_file": "toy_text_data/vocab/target.txt",
    "source_file": "toy_text_data/dev/source.txt",
    "target_file": "toy_text_data/dev/target.txt",
    "shuffle": False,
    "repeat": True,
    "max_length": 56,
    "delimiter": " ",
    "special_tokens_already_in_vocab": False,
  },
}

infer_params = {
  "batch_size_per_gpu": 1,
  "data_layer": ParallelTextDataLayer,
  "data_layer_params": {
    "src_vocab_file": "toy_text_data/vocab/source.txt",
    "tgt_vocab_file": "toy_text_data/vocab/source.txt",
    "source_file": "toy_text_data/test/source.txt",
    # this is intentional to be sure model is not using ground truth
    "target_file": "toy_text_data/test/source.txt",
    "shuffle": False,
    "repeat": False,
    "max_length": 256,
    "delimiter": " ",
    "special_tokens_already_in_vocab": False,
  },
}
