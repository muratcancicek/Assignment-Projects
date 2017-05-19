#
# This Python file is downloaded from https://github.com/tensorflow/tensorflow
# /blob/master/tensorflow/contrib/learn/python/learn/datasets/mnist.py
# and MODIFIED in order to read only testing MNIST set for CS466 assignment I 
# at Ozyegin University, Fall 2016
#

# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
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

"""Functions for downloading and reading MNIST data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from MainSrc.PythonVersionHandler import *
from Sparker.Logic.Trainer import *
from .DeepDataHandler import *
from paths import *
import os

from sklearn.preprocessing import StandardScaler
import numpy
#from six.moves import xrange  # pylint: disable=redefined-builtin

from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes

SOURCE_URL = 'http://yann.lecun.com/exdb/mnist/'

def _read32(bytestream):
  dt = numpy.dtype(numpy.uint32).newbyteorder('>')
  return numpy.frombuffer(bytestream.read(4), dtype=dt)[0]

class DataSet(object):
  def __init__(self,  images, labels, fake_data=False, one_hot=False, dtype=dtypes.float32, reshape=True):
    """Construct a DataSet.
    one_hot arg is used only if fake_data is true.  `dtype` can be either
    `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
    `[0, 1]`.
    """
    dtype = dtypes.as_dtype(dtype).base_dtype
    if dtype not in (dtypes.uint8, dtypes.float32):
      raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                      dtype)
    if fake_data:
      self._num_examples = 10000
      self.one_hot = one_hot
    else:
      assert images.shape[0] == labels.shape[0], (
          'images.shape: %s labels.shape: %s' % (images.shape, labels.shape))
      self._num_examples = images.shape[0]

      # Convert shape from [num examples, rows, columns, depth]
      # to [num examples, rows*columns] (assuming depth == 1)
      if reshape:
        assert images.shape[3] == 1
        images = images.reshape(images.shape[0],
                                images.shape[1] * images.shape[2])
      if dtype == dtypes.float32:
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(numpy.float32)
        images = numpy.multiply(images, 1.0 / 255.0)
    self._images = images
    self._labels = labels
    self._epochs_completed = 0
    self._index_in_epoch = 0

  @property
  def images(self):
    return self._images

  @property
  def labels(self):
    return self._labels

  @property
  def num_examples(self):
    return self._num_examples

  @property
  def epochs_completed(self):
    return self._epochs_completed

  def shuffle(self):
    all_data = numpy.c_[self._images.reshape(len(self._images), -1), self._labels.reshape(len(self._labels), -1)]
    numpy.random.shuffle(all_data)
    self._images = all_data[:, :self._images.size//len(self._images)].reshape(self._images.shape)
    self._labels = all_data[:, self._images.size//len(self._images):].reshape(self._labels.shape)

  def next_batch(self, batch_size, fake_data=False, shuffle=True):
    """Return the next `batch_size` examples from this data set."""
    if fake_data:
      fake_image = [1] * 784
      if self.one_hot:
        fake_label = [1] + [0] * 9
      else:
        fake_label = 0
      return [fake_image for _ in myXrange(batch_size)], [
          fake_label for _ in myXrange(batch_size)
      ]
    start = self._index_in_epoch
    # Shuffle for the first epoch
    if self._epochs_completed == 0 and start == 0 and shuffle:
      perm0 = numpy.arange(self._num_examples)
      numpy.random.shuffle(perm0)
      self._images = self._images[perm0]
      self._labels = self._labels[perm0]
    # Go to the next epoch
    if start + batch_size > self._num_examples:
      # Finished epoch
      self._epochs_completed += 1
      # Get the rest examples in this epoch
      rest_num_examples = self._num_examples - start
      images_rest_part = self._images[start:self._num_examples]
      labels_rest_part = self._labels[start:self._num_examples]
      # Shuffle the data
      if shuffle:
        perm = numpy.arange(self._num_examples)
        numpy.random.shuffle(perm)
        self._images = self._images[perm]
        self._labels = self._labels[perm]
      # Start next epoch
      start = 0
      self._index_in_epoch = batch_size - rest_num_examples
      end = self._index_in_epoch
      images_new_part = self._images[start:end]
      labels_new_part = self._labels[start:end]
      return numpy.concatenate((images_rest_part, images_new_part), axis=0) , numpy.concatenate((labels_rest_part, labels_new_part), axis=0)
    else:
      self._index_in_epoch += batch_size
      end = self._index_in_epoch
      return self._images[start:end], self._labels[start:end]

def generateDatasetsWithValidation(train_images, train_labels, test_images, test_labels, 
                                   dtype=dtypes.float32, reshape=False, validation_size=0): 
  if not 0 <= validation_size <= len(train_images):
    raise ValueError('Validation size should be between 0 and {}. Received: {}.'.format(len(train_images), validation_size))

  validation_images = train_images[:validation_size]
  validation_labels = train_labels[:validation_size]
  train_images = train_images[validation_size:]
  train_labels = train_labels[validation_size:]

  train = DataSet(train_images, train_labels, dtype=dtype, reshape=reshape)
  validation = DataSet(validation_images, validation_labels, dtype=dtype, reshape=reshape)
  test = DataSet(test_images, test_labels, dtype=dtype, reshape=reshape)

  return base.Datasets(train=train, validation=validation, test=test)

#def dense_to_one_hot(labels_dense, num_classes = 2):
#  """Convert class labels from scalars to one-hot vectors."""
#  num_labels = labels_dense.shape[0]
#  index_offset = numpy.arange(num_labels) * num_classes
#  labels_one_hot = numpy.zeros((num_labels, num_classes))
#  labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
#  return labels_one_hot

def dense_to_one_hot(labels_dense, num_classes = 2):
  labels_one_hot = []
  for i in labels_dense:
      o = [0 for m in range(num_classes)]
      o[int(i)] = 1
      labels_one_hot.append(o)
  return labels_one_hot

def read_gg_data_sets(train_dir, fake_data=False, one_hot=False, dtype=dtypes.float32, reshape=True,
                   validation_size=0, ratio = 0.7):
    allData = readTrainDataFromPickle(train_dir)
    print(allData[:3])
    test_labels = list(map(lambda x: x[0], allData))
    test_images = list(map(lambda x: x[1], allData))
    #print_(test_labels[:3])
    sepInd = int(len(test_labels) * ratio)
    #test_labels = dense_to_one_hot(test_labels, 2)
    test_labels = np.array(test_labels)
    scaler = StandardScaler(with_mean=True, with_std=True).fit(test_images)
    test_images = scaler.transform(test_images)
    test_images = np.array(test_images)
    train_images, train_labels = test_images[:sepInd], test_labels[:sepInd]
    test_images, test_labels = test_images[sepInd:], test_labels[sepInd:]
    validation_size = 0
    return generateDatasetsWithValidation(train_images, train_labels, test_images, test_labels, 
                                   dtype=dtype, reshape=reshape, validation_size=validation_size)


def load_trainDataset(train_dir='MNIST-data', path = '', reshape = False):
  return read_gg_data_sets(train_dir, one_hot=True, reshape = reshape)