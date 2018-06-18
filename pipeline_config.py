import os

from attrdict import AttrDict
from deepsense import neptune

from utils import read_params

ctx = neptune.Context()
params = read_params(ctx)

X_COLUMNS = ['comment_text_english']
assert params.filename_suffix == '_translated' and X_COLUMNS[0] == 'comment_text_english', """
if original, filename_suffix: '' data is used then X_COLUMNS should be set to 'comment_text' in the pipeline_config.py"""
Y_COLUMNS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
CV_LABELS = ['toxic']
ID_LABEL = ['id']

SOLUTION_CONFIG = AttrDict({
    'env': {'cache_dirpath': params.experiment_dir},
    'xy_splitter': {'x_columns': X_COLUMNS,
                    'y_columns': Y_COLUMNS
                    },
    'text_cleaner': {'drop_punctuation': bool(params.drop_punctuation),
                     'drop_newline': bool(params.drop_newline),
                     'drop_multispaces': bool(params.drop_multispaces),
                     'all_lower_case': bool(params.all_lower_case),
                     'fill_na_with': params.fill_na_with,
                     'deduplication_threshold': params.deduplication_threshold,
                     'anonymize': bool(params.anonymize),
                     'apostrophes': bool(params.apostrophes),
                     'use_stopwords': bool(params.use_stopwords)
                     },
    'bad_word_filter': {'word_list_filepath': params.bad_words_filepath},
    'char_tokenizer': {'char_level': True,
                       'maxlen': params.maxlen_char,
                       'num_words': params.max_features_char
                       },
    'word_tokenizer': {'char_level': False,
                       'maxlen': params.maxlen_words,
                       'num_words': params.max_features_word
                       },
    'tfidf_char_vectorizer': {'sublinear_tf': True,
                              'strip_accents': 'unicode',
                              'analyzer': 'char',
                              'token_pattern': r'\w{1,}',
                              'ngram_range': (1, params.char_ngram_max),
                              'max_features': params.max_features_char
                              },
    'tfidf_word_vectorizer': {'sublinear_tf': True,
                              'strip_accents': 'unicode',
                              'analyzer': 'word',
                              'token_pattern': r'\w{1,}',
                              'ngram_range': (1, 1),
                              'max_features': params.max_features_word
                              },
    'truncated_svd': {'n_components': params.truncated_svd__n_components},
    'embeddings': {'pretrained_filepath': params.embedding_filepath,
                   'max_features': params.max_features_word,
                   'embedding_size': params.word_embedding_size
                   },
    'dpcnn_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'trainable_embedding': bool(params.trainable_embedding),
                                                 'filter_nr': params.filter_nr,
                                                 'kernel_size': params.kernel_size,
                                                 'repeat_block': params.repeat_block,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'output_size': params.output_size,
                                                 'output_activation': params.output_activation,
                                                 'max_pooling': bool(params.max_pooling),
                                                 'mean_pooling': bool(params.mean_pooling),
                                                 'weighted_average_attention': bool(params.weighted_average_attention),
                                                 'concat_mode': params.concat_mode,
                                                 'dropout_embedding': params.dropout_embedding,
                                                 'conv_dropout': params.conv_dropout,
                                                 'dense_dropout': params.dense_dropout,
                                                 'dropout_mode': params.dropout_mode,
                                                 'conv_kernel_reg_l2': params.conv_kernel_reg_l2,
                                                 'conv_bias_reg_l2': params.conv_bias_reg_l2,
                                                 'dense_kernel_reg_l2': params.dense_kernel_reg_l2,
                                                 'dense_bias_reg_l2': params.dense_bias_reg_l2,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'batch_norm_first': bool(params.batch_norm_first),
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     'momentum': params.momentum,
                                                     'nesterov': True
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'shuffle': True,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'dpcnn_network',
                                     'best_model.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'unfreeze_layers': {'unfreeze_on_epoch': params.unfreeze_on_epoch},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {'model_name': 'dpcnn'},
        },
    },
    'scnn_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'trainable_embedding': bool(params.trainable_embedding),
                                                 'filter_nr': params.filter_nr,
                                                 'kernel_size': params.kernel_size,
                                                 'repeat_block': params.repeat_block,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'output_size': params.output_size,
                                                 'output_activation': params.output_activation,
                                                 'max_pooling': bool(params.max_pooling),
                                                 'mean_pooling': bool(params.mean_pooling),
                                                 'weighted_average_attention': bool(params.weighted_average_attention),
                                                 'concat_mode': params.concat_mode,
                                                 'dropout_embedding': params.dropout_embedding,
                                                 'conv_dropout': params.conv_dropout,
                                                 'dense_dropout': params.dense_dropout,
                                                 'dropout_mode': params.dropout_mode,
                                                 'conv_kernel_reg_l2': params.conv_kernel_reg_l2,
                                                 'conv_bias_reg_l2': params.conv_bias_reg_l2,
                                                 'dense_kernel_reg_l2': params.dense_kernel_reg_l2,
                                                 'dense_bias_reg_l2': params.dense_bias_reg_l2,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'batch_norm_first': bool(params.batch_norm_first),
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     'momentum': params.momentum,
                                                     'nesterov': True
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'shuffle': True,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'scnn_network',
                                     'best_model.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'unfreeze_layers': {'unfreeze_on_epoch': params.unfreeze_on_epoch},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {'model_name': 'scnn'},
        },
    },
    'lstm_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'trainable_embedding': bool(params.trainable_embedding),
                                                 'unit_nr': params.filter_nr,
                                                 'repeat_block': params.repeat_block,
                                                 'max_pooling': bool(params.max_pooling),
                                                 'mean_pooling': bool(params.mean_pooling),
                                                 'weighted_average_attention': bool(params.weighted_average_attention),
                                                 'concat_mode': params.concat_mode,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'dropout_embedding': params.dropout_embedding,
                                                 'rnn_dropout': params.rnn_dropout,
                                                 'dense_dropout': params.dense_dropout,
                                                 'output_size': params.output_size,
                                                 'output_activation': params.output_activation,
                                                 'dropout_mode': params.dropout_mode,
                                                 'rnn_kernel_reg_l2': params.rnn_kernel_reg_l2,
                                                 'rnn_recurrent_reg_l2': params.rnn_kernel_reg_l2,
                                                 'rnn_bias_reg_l2': params.rnn_bias_reg_l2,
                                                 'dense_kernel_reg_l2': params.dense_kernel_reg_l2,
                                                 'dense_bias_reg_l2': params.dense_bias_reg_l2,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'batch_norm_first': bool(params.batch_norm_first),
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     'momentum': params.momentum,
                                                     'nesterov': True
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'lstm_network',
                                     'best_model.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'unfreeze_layers': {'unfreeze_on_epoch': params.unfreeze_on_epoch},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {'model_name': 'lstm'},
        },
    },
    'gru_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_word,
                                                 'maxlen': params.maxlen_words,
                                                 'embedding_size': params.word_embedding_size,
                                                 'trainable_embedding': bool(params.trainable_embedding),
                                                 'unit_nr': params.filter_nr,
                                                 'repeat_block': params.repeat_block,
                                                 'max_pooling': bool(params.max_pooling),
                                                 'mean_pooling': bool(params.mean_pooling),
                                                 'weighted_average_attention': bool(params.weighted_average_attention),
                                                 'concat_mode': params.concat_mode,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'dropout_embedding': params.dropout_embedding,
                                                 'rnn_dropout': params.rnn_dropout,
                                                 'dense_dropout': params.dense_dropout,
                                                 'output_size': params.output_size,
                                                 'output_activation': params.output_activation,
                                                 'dropout_mode': params.dropout_mode,
                                                 'rnn_kernel_reg_l2': params.rnn_kernel_reg_l2,
                                                 'rnn_recurrent_reg_l2': params.rnn_kernel_reg_l2,
                                                 'rnn_bias_reg_l2': params.rnn_bias_reg_l2,
                                                 'dense_kernel_reg_l2': params.dense_kernel_reg_l2,
                                                 'dense_bias_reg_l2': params.dense_bias_reg_l2,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'batch_norm_first': bool(params.batch_norm_first),
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     'momentum': params.momentum,
                                                     'nesterov': True
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'gru_network',
                                     'best_model.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'unfreeze_layers': {'unfreeze_on_epoch': params.unfreeze_on_epoch},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {'model_name': 'gru'},
        },
    },
    'char_vdcnn_network': {
        'architecture_config': {'model_params': {'max_features': params.max_features_char,
                                                 'maxlen': params.maxlen_char,
                                                 'embedding_size': params.char_embedding_size,
                                                 'filter_nr': params.filter_nr,
                                                 'kernel_size': params.kernel_size,
                                                 'repeat_block': params.repeat_block,
                                                 'dense_size': params.dense_size,
                                                 'repeat_dense': params.repeat_dense,
                                                 'max_pooling': bool(params.max_pooling),
                                                 'mean_pooling': bool(params.mean_pooling),
                                                 'weighted_average_attention': bool(params.weighted_average_attention),
                                                 'concat_mode': params.concat_mode,
                                                 'dropout_embedding': params.dropout_embedding,
                                                 'conv_dropout': params.conv_dropout,
                                                 'dense_dropout': params.dense_dropout,
                                                 'output_size': params.output_size,
                                                 'output_activation': params.output_activation,
                                                 'dropout_mode': params.dropout_mode,
                                                 'conv_kernel_reg_l2': params.conv_kernel_reg_l2,
                                                 'conv_bias_reg_l2': params.conv_bias_reg_l2,
                                                 'dense_kernel_reg_l2': params.dense_kernel_reg_l2,
                                                 'dense_bias_reg_l2': params.dense_bias_reg_l2,
                                                 'use_prelu': bool(params.use_prelu),
                                                 'use_batch_norm': bool(params.use_batch_norm),
                                                 'batch_norm_first': bool(params.batch_norm_first),
                                                 },
                                'optimizer_params': {'lr': params.lr,
                                                     'momentum': params.momentum,
                                                     'nesterov': True
                                                     },
                                },
        'training_config': {'epochs': params.epochs_nr,
                            'batch_size': params.batch_size_train,
                            },
        'callbacks_config': {'model_checkpoint': {
            'filepath': os.path.join(params.experiment_dir, 'checkpoints',
                                     'char_vdcnn_network',
                                     'best_model.h5'),
            'save_best_only': True,
            'save_weights_only': False},
            'lr_scheduler': {'gamma': params.gamma},
            'unfreeze_layers': {'unfreeze_on_epoch': params.unfreeze_on_epoch},
            'early_stopping': {'patience': params.patience},
            'neptune_monitor': {'model_name': 'char_vdcnn'},
        },
    },
    'xgboost_ensemble': {'label_nr': 6,
                         'objective': params.xgboost__objective,
                         'eval_metric': params.xgboost__eval_metric,
                         'scale_pos_weight': params.xgboost__scale_pos_weight,
                         'n_estimators': params.xgboost__n_estimators,
                         'learning_rate': params.xgboost__learning_rate,
                         'max_depth': params.xgboost__max_depth,
                         'min_child_weight': params.xgboost__min_child_weight,
                         'gamma': params.xgboost__gamma,
                         'colsample_bytree': params.xgboost__colsample_bytree,
                         'subsample': params.xgboost__subsample,
                         'reg_lambda': params.xgboost__reg_lambda,
                         'reg_alpha': params.xgboost__reg_alpha,
                         'n_jobs': params.num_workers},
    'clipper': {'lower': eval(params.clipper__lower),
                'upper': eval(params.clipper__upper)}
})
