import tensorflow as tf

# Process images of this size. Note that this differs from the original CIFAR
# image size of 32 x 32. If one alters this number, then the entire model
# architecture will change and any model would need to be retrained.
IMAGE_SIZE = 32

# Global constants describing the CIFAR-10 data set.
NUM_CLASSES = 10
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 50000
NUM_EXAMPLES_PER_EPOCH_FOR_EVAL = 10000

FLAGS = tf.app.flags.FLAGS

# Basic model parameters.
batch_size = 128
data_dir = '/tmp/cifar10_data'
use_fp16 = False

train_dir = '/tmp/cifar10_train'
max_steps = 30
log_device_placement = False
log_frequency = 100

#FLAGS = tf.app.flags.FLAGS
#if COMPUTERNAME == 'MSI' or COMPUTERNAME == 'LM-IST-00UBFVH8' or COMPUTERNAME == 'server':
#    # Basic model parameters.
#    tf.app.flags.DEFINE_integer('batch_size', 128, """Number of images to process in a batch.""")
#    tf.app.flags.DEFINE_string('data_dir', '/tmp/cifar10_data', """Path to the CIFAR-10 data directory.""")
#    tf.app.flags.DEFINE_boolean('use_fp16', False, """Train the model using fp16.""")

#    tf.app.flags.DEFINE_string('train_dir', '/tmp/cifar10_train', """Directory where to write event logs and checkpoint.""")
#    tf.app.flags.DEFINE_integer('max_steps', 300, """Number of batches to run.""")
#    tf.app.flags.DEFINE_boolean('log_device_placement', False, """Whether to log device placement.""")
#    tf.app.flags.DEFINE_integer('log_frequency', 1000, """How often to log results to the console.""")

# Constants describing the training process.
MOVING_AVERAGE_DECAY = 0.9999     # The decay to use for the moving average.
NUM_EPOCHS_PER_DECAY = 350.0      # Epochs after which learning rate decays.
LEARNING_RATE_DECAY_FACTOR = 0.1  # Learning rate decay factor.
INITIAL_LEARNING_RATE = 0.1       # Initial learning rate.

# If a model is trained with multiple GPUs, prefix all Op names with tower_name
# to differentiate the operations. Note that this prefix is removed from the
# names of the summaries when visualizing a model.
TOWER_NAME = 'tower'
num_gpus = 2

DATA_URL = 'http://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz'

eval_dir = './tmp/cifar10_eval'
eval_data = 'test'
checkpoint_dir = './tmp/cifar10_train'
eval_interval_secs = 60 * 5
num_examples = 1000
run_once = True


from PythonVersionHandler import *
import cifar10_input
import cifar10
import MyModel
