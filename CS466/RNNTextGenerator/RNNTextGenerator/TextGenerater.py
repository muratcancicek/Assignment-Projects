
'''
Save and Restore a model using TensorFlow.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import print_function
import tensorflow as tf
import numpy as np

from PythonVersionHandler import *
from paths import *
import reader

import tensorflow as tf

from ptb_word_lm import *

class CustomConfig(object):
    """Custom config."""
    is_char_model = True
    optimizer = 'AdamOptimizer'
    init_scale = 0.004
    learning_rate = 0.80
    max_grad_norm = 17
    num_layers = 2
    num_steps = 20
    hidden_size = 200
    max_epoch = 14
    max_max_epoch = 1024
    keep_prob = 0.5
    lr_decay = 1 / 1.15
    batch_size = 64
    vocab_size = 27486

def main(customConfig = CustomConfig):
    if not FLAGS.data_path:
        raise ValueError("Must set --data_path to PTB data directory")

    raw_data = reader.ptb_raw_data(FLAGS.data_path, FLAGS.file_prefix)
    train_data, valid_data, test_data, word_to_id, id_2_word = raw_data
    vocab_size = len(word_to_id)
    #print(word_to_id)
    print_('Distinct terms: %d' % vocab_size)
    config = get_config() if customConfig == None else customConfig()
    config.vocab_size = config.vocab_size if config.vocab_size < vocab_size else vocab_size
    eval_config = get_config() if customConfig == None else customConfig()
    eval_config.vocab_size = eval_config.vocab_size if eval_config.vocab_size < vocab_size else vocab_size
    eval_config.batch_size = 1
    eval_config.num_steps = 1

    if config.is_char_model:
        seed_for_sample = [c for c in FLAGS.seed_for_sample.replace(' ', '_')]
    else:
        seed_for_sample = FLAGS.seed_for_sample.split()
        
    with tf.Graph().as_default():
        initializer = tf.random_uniform_initializer(-config.init_scale, config.init_scale)

        with tf.name_scope("Test"):
            with tf.variable_scope("Model", reuse=False, initializer=initializer):
                mtest = PTBModel(is_training=False, config=eval_config)

        saver = tf.train.Saver(name='saver', write_version=tf.train.SaverDef.V2)
        sv = tf.train.Supervisor(logdir=FLAGS.save_path, save_model_secs=0, save_summaries_secs=0, saver=saver)

        with sv.managed_session() as session: 
            # Restore model weights from previously saved modelcheckpoint
            saver.restore(session, 'data/tensorflow/1024X14_64/graph.pbtxt')
            print("Model restored from file: %s" % save_path)

            print_(nowStr()+':', "Seed: %s" % pretty_print([word_to_id[x] for x in seed_for_sample], config.is_char_model, id_2_word))
            print_(nowStr()+':', "Sample: %s" % pretty_print(do_sample(session, mtest, [word_to_id[word] for word in seed_for_sample], max(5 * (len(seed_for_sample) + 1), 10)), config.is_char_model, id_2_word))
            test_perplexity = run_epoch(session, mtest, test_data)
            print_(nowStr()+':', "Test Perplexity: %.3f" % test_perplexity)
    tf.app.run()