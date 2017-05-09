# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Evaluation for CIFAR-10.
Accuracy:
cifar10_train.py achieves 83.0% accuracy after 100K steps (256 epochs
of data) as judged by cifar10_eval.py.
Speed:
On a single Tesla K40, cifar10_train.py processes a single batch of 128 images
in 0.25-0.35 sec (i.e. 350 - 600 images /sec). The model reaches ~86%
accuracy after 100K steps in 8 hours of training time.
Usage:
Please see the tutorial and website for how to download the CIFAR-10
data set, compile the program and train the model.
http://tensorflow.org/tutorials/deep_cnn/
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from datetime import datetime
import math
import time

import numpy as np
import tensorflow as tf

import model as cifar10
import model2 as cifar10_2

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('eval_dir', '/Users/Furkan/Desktop/tmp_50k/cifar10_eval',
                           """Directory where to write event logs.""")
tf.app.flags.DEFINE_string('eval_dir2', '/Users/Furkan/Desktop/tmp2/cifar10_eval',
                           """Directory where to write event logs.""")
tf.app.flags.DEFINE_string('eval_data', 'test',
                           """Either 'test' or 'train_eval'.""")
tf.app.flags.DEFINE_string('checkpoint_dir', '/Users/Furkan/Desktop/tmp_50k/cifar10_train',
                           """Directory where to read model checkpoints.""")
tf.app.flags.DEFINE_string('checkpoint_dir2', '/Users/Furkan/Desktop/tmp2/cifar10_train',
                           """Directory where to read model checkpoints.""")
tf.app.flags.DEFINE_integer('eval_interval_secs', 60 * 5,
                            """How often to run the eval.""")
tf.app.flags.DEFINE_integer('num_examples', 10000,
                            """Number of examples to run.""")
tf.app.flags.DEFINE_boolean('run_once', True,
                            """Whether to run eval only once.""")


def eval_once(network, saver, summary_writer, top_k_op, summary_op, checkpoint_dir):
    with tf.Session() as sess:
        preds = []
        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1]
        else:
            print('No checkpoint file found')
            return

        # Start the queue runners.
        coord = tf.train.Coordinator()
        try:
            threads = []
            for qr in tf.get_collection(tf.GraphKeys.QUEUE_RUNNERS):
                threads.extend(qr.create_threads(sess, coord=coord, daemon=True,
                                                 start=True))

            num_iter = int(math.ceil(FLAGS.num_examples / FLAGS.batch_size))
            true_count = 0  # Counts the number of correct predictions.
            total_sample_count = num_iter * FLAGS.batch_size
            step = 0

            while step < num_iter and not coord.should_stop():
                predictions = sess.run([top_k_op])
                true_count += np.sum(predictions)
                for i in range(len(predictions)):
                    for j in range(len(predictions[i])):
                        preds.append(predictions[i][j])
                step += 1

            # Compute precision @ 1.
            total_parameters = 0
            for variable in tf.trainable_variables():
                # shape is an array of tf.Dimension
                shape = variable.get_shape()
                variable_parametes = 1
                for dim in shape:
                    variable_parametes *= dim.value
                total_parameters += variable_parametes

            print('\n Network-%s:' % str(network))
            print('\n')
            print("%s: Total parameters @ 1 = %d" % (datetime.now(), total_parameters))

            precision = true_count / total_sample_count
            print('%s: Total @ 1 = %d' % (datetime.now(), total_sample_count))
            print('%s: Correct @ 1 = %d' % (datetime.now(), true_count))
            print('%s: Wrong @ 1 = %d' % (datetime.now(), (total_sample_count - true_count)))
            print('%s: Precision @ 1 = %.3f' % (datetime.now(), precision))

            summary = tf.Summary()
            summary.ParseFromString(sess.run(summary_op))
            summary.value.add(tag='Precision @ 1', simple_value=precision)
            summary_writer.add_summary(summary, global_step)

        except Exception as e:  # pylint: disable=broad-except
            coord.request_stop(e)

        coord.request_stop()
        coord.join(threads, stop_grace_period_secs=10)

        return preds


def evaluate(network, checkpoint_dir):
    """Eval CIFAR-10 for a number of steps."""
    with tf.Graph().as_default() as g:
        # Get images and labels for CIFAR-10.
        eval_data = FLAGS.eval_data == 'test'

        if network == 1:
            images, labels = cifar10.inputs(eval_data=eval_data)
            logits, w1, b1, w2, b2 = cifar10.inference(images)
        else:
            images, labels = cifar10_2.inputs(eval_data=eval_data)
            logits, w1, b1, w2, b2 = cifar10_2.inference(images)

        # Calculate predictions.
        top_k_op = tf.nn.in_top_k(logits, labels, 1)

        # Restore the moving average version of the learned variables for eval.
        variable_averages = tf.train.ExponentialMovingAverage(
            cifar10.MOVING_AVERAGE_DECAY)
        variables_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variables_to_restore)

        # Build the summary operation based on the TF collection of Summaries.
        summary_op = tf.summary.merge_all()

        summary_writer = tf.summary.FileWriter(FLAGS.eval_dir, g)

        preds = eval_once(network, saver, summary_writer, top_k_op, summary_op, checkpoint_dir)
        """while True:
            eval_once(saver, summary_writer, top_k_op, summary_op)
            if FLAGS.run_once:
                break
            time.sleep(FLAGS.eval_interval_secs)"""

        return preds


def apply_mcnemar_test(labels1, labels2):
    pos_pos = pos_neg = neg_pos = neg_neg = 0

    for idx, lab1 in enumerate(labels1):
        lab2 = labels2[idx]

        if lab2:
            if lab1: pos_pos +=1
            else: pos_neg +=1
        else:
            if not lab1: neg_neg +=1
            else: neg_pos +=1

    return np.asarray([[pos_pos, pos_neg],[neg_pos, neg_neg]])


def main(argv=None):  # pylint: disable=unused-argument
    cifar10.maybe_download_and_extract()
    if tf.gfile.Exists(FLAGS.eval_dir):
        tf.gfile.DeleteRecursively(FLAGS.eval_dir)
    tf.gfile.MakeDirs(FLAGS.eval_dir)

    model1_dir = '/Users/Furkan/Desktop/tmp_50k/cifar10_train'
    model2_dir = '/Users/Furkan/Desktop/tmp2/cifar10_train'

    label_array1 = evaluate(1, model1_dir)
    label_array2 = evaluate(2, model2_dir)

    mcnemar_test = apply_mcnemar_test(label_array1, label_array2)

    print("\n McNemar's Test: \n")
    print("\t Both correct: %s" % str(mcnemar_test[0][0]))
    print("\t Both wrong: %s" % str(mcnemar_test[1][1]))
    print("\t Only network-1 correct: %s" % str(mcnemar_test[0][1]))
    print("\t Only network-2 correct: %s" % str(mcnemar_test[1][0]))


if __name__ == '__main__':
    tf.app.run()
