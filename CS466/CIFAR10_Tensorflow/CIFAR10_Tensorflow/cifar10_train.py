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

"""A binary to train CIFAR-10 using a single GPU.
Accuracy:
cifar10_train.py achieves ~86% accuracy after 100K steps (256 epochs of
data) as judged by cifar10_eval.py.
Speed: With batch_size 128.
System          | Step Time (sec/batch)    |     Accuracy
------------------------------------------------------------------
1 Tesla K20m    | 0.35-0.60                | ~86% at 60K steps    (5 hours)
1 Tesla K40m    | 0.25-0.35                | ~86% at 100K steps (4 hours)
Usage:
Please see the tutorial and website for how to download the CIFAR-10
data set, compile the program and train the model.
http://tensorflow.org/tutorials/deep_cnn/
"""

from PythonVersionHandler import *
from paths import *
import cifar10
import tfFLAGS 
import MyModel
import MyModel2


def train():
    """Train CIFAR-10 for a number of steps."""
    with tf.Graph().as_default():
        global_step = tf.contrib.framework.get_or_create_global_step()

        # Get images and labels for CIFAR-10.
        images, labels = cifar10.distorted_inputs()

        # Build a Graph that computes the logits predictions from the
        # inference model.
        if tfFLAGS.network == 1:
            images, labels = cifar10.distorted_inputs()
            logits, fc1_w, fc1_b, fc2_w, fc2_b = MyModel.inference(images)
        else:
            images, labels = cifar10.distorted_inputs()
            logits, fc1_w, fc1_b, fc2_w, fc2_b = MyModel2.inference(images)

        # Calculate loss.
        loss = cifar10.loss(logits, labels)

            # L2 regularization for the fully connected parameters.
        regularizers = (tf.nn.l2_loss(fc1_w) + tf.nn.l2_loss(fc1_b) + tf.nn.l2_loss(fc2_w) + tf.nn.l2_loss(fc2_b))

        # Add the regularization term to the loss.
        loss += 5e-4 * regularizers

        # Build a Graph that trains the model with one batch of examples and
        # updates the model parameters.
        train_op = cifar10.train(loss, global_step)

        class _LoggerHook(tf.train.SessionRunHook):
            """Logs loss and runtime."""

            def begin(self):
                self._step = -1
                self._start_time = time.time()

            def before_run(self, run_context):
                self._step += 1
                return tf.train.SessionRunArgs(loss)    # Asks for loss value.

            def after_run(self, run_context, run_values):
                if self._step % tfFLAGS.log_frequency == 0:
                    current_time = time.time()
                    duration = current_time - self._start_time
                    self._start_time = current_time

                    loss_value = run_values.results
                    examples_per_sec = tfFLAGS.log_frequency * tfFLAGS.batch_size / duration
                    sec_per_batch = float(duration / tfFLAGS.log_frequency)

                    format_str = ('%s: step %d, loss = %.2f (%.1f examples/sec; %.3f '
                                                'sec/batch)')
                    print_(format_str % (datetime.now(), self._step, loss_value, examples_per_sec, sec_per_batch))
        
        texts = ['conv1:', 'conv1Biases:', 'conv2:', 'conv2Biases:', 'local3:', 'local3Biases:', 'local4:', 'local4Biases:', 'softmax:', 'softmaxBiases:']
        total_parameters = 0; count = 0
        for variable in tf.trainable_variables():
            variable_parametes = 1
            for dim in variable.get_shape():
                    variable_parametes *= dim.value
            print('Number of hidden parameters of ' + texts[count], variable_parametes)
            total_parameters += variable_parametes
            count += 1
        print('Total Number of hidden parameters:', total_parameters)

        with tf.train.MonitoredTrainingSession(checkpoint_dir=tfFLAGS.train_dir,
                hooks=[tf.train.StopAtStepHook(last_step=tfFLAGS.max_steps), tf.train.NanTensorHook(loss),_LoggerHook()],
                config=tf.ConfigProto( device_count = {'GPU': 0}, log_device_placement=tfFLAGS.log_device_placement)) as mon_sess:
            while not mon_sess.should_stop():
                mon_sess.run(train_op)


def main(argv=None):    # pylint: disable=unused-argument
    cifar10.maybe_download_and_extract()
    if tf.gfile.Exists(tfFLAGS.train_dir):
        tf.gfile.DeleteRecursively(tfFLAGS.train_dir)
    tf.gfile.MakeDirs(tfFLAGS.train_dir)
    train()


if __name__ == '__main__':
    tf.app.run()