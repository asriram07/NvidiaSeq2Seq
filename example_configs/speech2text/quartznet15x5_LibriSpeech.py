# pylint: skip-file
# QuartzNet paper: https://arxiv.org/abs/1910.10261
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from open_seq2seq.models import Speech2Text
from open_seq2seq.encoders import TDNNEncoder
from open_seq2seq.decoders import FullyConnectedCTCDecoder
from open_seq2seq.data.speech2text.speech2text import Speech2TextDataLayer
from open_seq2seq.losses import CTCLoss
from open_seq2seq.optimizers.lr_policies import cosine_decay
from open_seq2seq.optimizers.novograd import NovoGrad

residual_dense = False  # Enable or disable Dense Residual

base_model = Speech2Text

base_params = {
    "random_seed": 0,
    "use_horovod": True,
    "num_epochs": 400,

    "num_gpus": 8,
    "batch_size_per_gpu": 32,
    "iter_size": 1,

    "save_summaries_steps": 100,
    "print_loss_steps": 10,
    "print_samples_steps": 2200,
    "eval_steps": 2200,
    "save_checkpoint_steps": 1100,
    "logdir": "jasper_log_folder",
    "num_checkpoints": 2,

    "optimizer": NovoGrad,
    "optimizer_params": {
        "beta1": 0.95,
        "beta2": 0.5,
        "epsilon": 1e-08,
        "weight_decay": 0.001,
        "grad_averaging": False,
    },
    "lr_policy": cosine_decay,
    "lr_policy_params": {
        "learning_rate": 0.01,
        "min_lr": 0.0,
        "warmup_steps": 1000
    },

    "dtype": tf.float32,
    # "loss_scaling": "Backoff",

    "summaries": ['learning_rate', 'variables', 'gradients', 'larc_summaries',
                  'variable_norm', 'gradient_norm', 'global_gradient_norm'],

    "encoder": TDNNEncoder,
    "encoder_params": {
        "convnet_layers": [
            {
                "type": "sep_conv1d", "repeat": 1,
                "kernel_size": [33], "stride": [2],
                "num_channels": 256, "padding": "SAME",
                "dilation":[1]
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [33], "stride": [1],
                "num_channels": 256, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [33], "stride": [1],
                "num_channels": 256, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [33], "stride": [1],
                "num_channels": 256, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [39], "stride": [1],
                "num_channels": 256, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [39], "stride": [1],
                "num_channels": 256, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [39], "stride": [1],
                "num_channels": 256, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [51], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [51], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [51], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [63], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [63], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [63], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [75], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [75], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 5,
                "kernel_size": [75], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[1],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "sep_conv1d", "repeat": 1,
                "kernel_size": [87], "stride": [1],
                "num_channels": 512, "padding": "SAME",
                "dilation":[2],
                "residual": True, "residual_dense": residual_dense
            },
            {
                "type": "conv1d", "repeat": 1,
                "kernel_size": [1], "stride": [1],
                "num_channels": 1024, "padding": "SAME",
                "dilation":[1]
            }
        ],

        "dropout_keep_prob": 1.0,

        "initializer": tf.contrib.layers.xavier_initializer,
        "initializer_params": {
            'uniform': False,
        },
        "normalization": "batch_norm",
        "activation_fn": tf.nn.relu,
        "data_format": "channels_last",
        "use_conv_mask": True,
    },

    "decoder": FullyConnectedCTCDecoder,
    "decoder_params": {
        "initializer": tf.contrib.layers.xavier_initializer,
        "use_language_model": False,
        "infer_logits_to_pickle": False,
    },
    "loss": CTCLoss,
    "loss_params": {},

    "data_layer": Speech2TextDataLayer,
    "data_layer_params": {
        "num_audio_features": 64,
        "input_type": "logfbank",
        "vocab_file": "open_seq2seq/test_utils/toy_speech_data/vocab.txt",
        "norm_per_feature": True,
        "window": "hanning",
        "precompute_mel_basis": True,
        "sample_freq": 16000,
        "pad_to": 16,
        "dither": 1e-5,
        "backend": "librosa",
    },
}

train_params = {
    "data_layer": Speech2TextDataLayer,
    "data_layer_params": {
        "augmentation": {
            'n_freq_mask': 2,
            'n_time_mask': 2,
            'width_freq_mask': 6,
            'width_time_mask': 6,
        },
        "dataset_files": [
            "/data/librispeech/librivox-train-clean-100.csv",
            "/data/librispeech/librivox-train-clean-360.csv",
            "/data/librispeech/librivox-train-other-500.csv"
        ],
        "max_duration": 16.7,
        "shuffle": True,
    },
}

eval_params = {
    "data_layer": Speech2TextDataLayer,
    "data_layer_params": {
        "dataset_files": [
            "/data/librispeech/librivox-dev-clean.csv",
        ],
        "shuffle": False,
    },
}

infer_params = {
    "data_layer": Speech2TextDataLayer,
    "data_layer_params": {
        "dataset_files": [
            "/data/librispeech/librivox-test-clean.csv",
        ],
        "shuffle": False,
    },
}
