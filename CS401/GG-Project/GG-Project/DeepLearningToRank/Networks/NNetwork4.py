from .NNetwork1 import *
from DeepLearningToRank import tfFLAGS

# Architecture of model
conv1Size = 2; conv1Out = 4; conv1Shape = [conv1Size, conv1Size, 3, conv1Out]
conv2Size = 2; conv2Shape = [conv2Size, conv2Size, conv1Out, 10]

inputNeurons = tfFLAGS.IMAGE_SIZE;
hidden1Neurons = 64
hidden2Neurons = 256
hidden3Neurons = 1024
hidden4Neurons = 4096
hidden5Neurons = 512
hidden6Neurons = 32
hidden7Neurons = 12
outputNeurons = tfFLAGS.NUM_CLASSES

def summarizeModel():
    print_('(%d) x %d x %d x %d x %d x %d x %d x %d x (%d)' % 
           (inputNeurons, hidden1Neurons, hidden2Neurons, hidden3Neurons, hidden4Neurons, hidden5Neurons, hidden6Neurons, hidden7Neurons, outputNeurons) )

def network(images):

    # local1
    with tf.variable_scope('local1') as scope:
        fc1_weights = variable_with_weight_decay('weights', shape=[inputNeurons, hidden1Neurons], stddev=0.04, wd=0.004)
        fc1_biases = variable_on_cpu('biases', [hidden1Neurons], tf.constant_initializer(0.1))
        local1 = tf.nn.relu(tf.matmul(images, fc1_weights) + fc1_biases, name=scope.name)        
        activation_summary(local1)

    # local2
    with tf.variable_scope('local2') as scope:
        fc2_weights = variable_with_weight_decay('weights', shape=[hidden1Neurons, hidden2Neurons], stddev=0.04, wd=0.004)
        fc2_biases = variable_on_cpu('biases', [hidden2Neurons], tf.constant_initializer(0.1))
        local2 = tf.nn.relu(tf.matmul(local1, fc2_weights) + fc2_biases, name=scope.name)
        activation_summary(local2)

    # local3
    with tf.variable_scope('local3') as scope:
        fc1_weights = variable_with_weight_decay('weights', shape=[hidden2Neurons, hidden3Neurons], stddev=0.04, wd=0.004)
        fc1_biases = variable_on_cpu('biases', [hidden3Neurons], tf.constant_initializer(0.1))
        local3 = tf.nn.relu(tf.matmul(local2, fc1_weights) + fc1_biases, name=scope.name)        
        activation_summary(local3)

    # local4
    with tf.variable_scope('local4') as scope:
        fc2_weights = variable_with_weight_decay('weights', shape=[hidden3Neurons, hidden4Neurons], stddev=0.04, wd=0.004)
        fc2_biases = variable_on_cpu('biases', [hidden4Neurons], tf.constant_initializer(0.1))
        local4 = tf.nn.relu(tf.matmul(local3, fc2_weights) + fc2_biases, name=scope.name)
        activation_summary(local4)

    # local5
    with tf.variable_scope('local5') as scope:
        fc1_weights = variable_with_weight_decay('weights', shape=[hidden4Neurons, hidden5Neurons], stddev=0.04, wd=0.004)
        fc1_biases = variable_on_cpu('biases', [hidden5Neurons], tf.constant_initializer(0.1))
        local5 = tf.nn.relu(tf.matmul(local4, fc1_weights) + fc1_biases, name=scope.name)        
        activation_summary(local5)

    # local6
    with tf.variable_scope('local6') as scope:
        fc2_weights = variable_with_weight_decay('weights', shape=[hidden5Neurons, hidden6Neurons], stddev=0.04, wd=0.004)
        fc2_biases = variable_on_cpu('biases', [hidden6Neurons], tf.constant_initializer(0.1))
        local6 = tf.nn.relu(tf.matmul(local5, fc2_weights) + fc2_biases, name=scope.name)
        activation_summary(local6)
        
    # local7
    with tf.variable_scope('local7') as scope:
        fc2_weights = variable_with_weight_decay('weights', shape=[hidden6Neurons, hidden7Neurons], stddev=0.04, wd=0.004)
        fc2_biases = variable_on_cpu('biases', [hidden7Neurons], tf.constant_initializer(0.1))
        local7 = tf.nn.relu(tf.matmul(local6, fc2_weights) + fc2_biases, name=scope.name)
        activation_summary(local7)
        
    with tf.variable_scope('softmax_linear') as scope:
        weights = variable_with_weight_decay('weights', [hidden7Neurons, outputNeurons], stddev=1/192.0, wd=0.0)
        biases = variable_on_cpu('biases', [outputNeurons], tf.constant_initializer(0.0))
        softmax_linear = tf.add(tf.matmul(local7, weights), biases, name=scope.name)
        activation_summary(softmax_linear)

    return softmax_linear, fc1_weights, fc1_biases, fc2_weights, fc2_biases
