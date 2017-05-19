from MainSrc.PythonVersionHandler import *
import tensorflow as tf
from . import tfFLAGS 
from paths import *
import time
import math

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W, stride = 1):
  return tf.nn.conv2d(x, W, strides=[stride, stride, stride, stride], padding='SAME')

def downsample(x, n = 2):
    return tf.nn.avg_pool(x, ksize=[1, n, n, 1], strides=[1, n, n, 1], padding='SAME')

def max_pool(x, n = 2):
  return tf.nn.max_pool(x, ksize=[1, n, n, 1], strides=[1, n, n, 1], padding='SAME')

def buildBiasedLayers(input, shape, transaction = tf.matmul, activationFunction = tf.nn.relu):#lambda x: x): # activationFunction = None 
    weight = weight_variable(shape)
    bias = bias_variable([shape[-1]])
    output = transaction(input, weight)
    output = activationFunction(output + bias)
    return output

def buildConvReluMaxPoolLayers(input, patch, inputChannel, outputChannel, poolSize = 2):
    shape = [patch, patch, inputChannel, outputChannel]
    h_conv = buildBiasedLayers(input, shape, conv2d, tf.nn.relu)
    output = max_pool(h_conv, n = poolSize)
    return output
     
def dropoutLayer(x):
    keep_prob = tf.placeholder(tf.float32)
    return tf.nn.dropout(x, keep_prob)

def buildFullyConnectedLayers(input, inputChannel, outputChannel):
    shape = [inputChannel, outputChannel]
    #flat_input = tf.reshape(input, [-1, shape[0]])flat_
    output = buildBiasedLayers(input, shape, tf.matmul)
    return output
     
def inputLayer(x, xSize, downsampling = False, poolSize = 2, patch = 5, outputBridge = 196):
    shape = [1, outputBridge]
    flat_input = tf.reshape(x, [-1, shape[0]])
    output = buildBiasedLayers(flat_input, shape, tf.matmul)
    return output, outputBridge, 1

def hiddenLayer1(input, inputBridge, n, patch = 5, poolSize = 2, outputBridge = 64):
    #output = buildConvReluMaxPoolLayers(input, patch, inputBridge, outputBridge, poolSize) 
    output = buildFullyConnectedLayers(input, n * n * inputBridge, outputBridge) 
    n = int(n/poolSize)
    #print_('Output:', output, outputBridge, n)
    return output, outputBridge, n

def hiddenLayer2(input, inputBridge, n, outputBridge = 1024):
    output = buildFullyConnectedLayers(input, n * n * inputBridge, outputBridge) 
    n = 1
    return output, outputBridge, n

def lastLayer(input, inputBridge, n):
    output = dropoutLayer(input)
    output = buildFullyConnectedLayers(input, n * n * inputBridge, 2)
    return output

def firstCNN(x, xSize, downsampling = False):

    output, outputBridge, n = inputLayer(x, xSize, downsampling = downsampling,
                                         poolSize = 2, patch = 5, outputBridge = 32)

    output, outputBridge, n = hiddenLayer1(output, outputBridge, n, 
                                           poolSize = 2, patch = 5, outputBridge = 64)

    output, outputBridge, n = hiddenLayer2(output, outputBridge, n, outputBridge = 64)

    return lastLayer(output, outputBridge, n)

def secondCNN(x, xSize, downsampling = False):

    output, outputBridge, n = inputLayer(x, xSize, downsampling = downsampling,
                                          poolSize = 2, patch = 7, outputBridge = 64)

    output, outputBridge, n = hiddenLayer1(output, outputBridge, n, 
                                           poolSize = 2, patch = 9, outputBridge = 128)

    output, outputBridge, n = hiddenLayer2(output, outputBridge, n, outputBridge = 1024)

    return lastLayer(output, outputBridge, n)

def runCFirstCustomCNN(mnist, x, y_, xSize = 784, iterations = 1000, cnn = firstCNN, downsampling = False, text = 'First Custom CNN running...'):
    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    print_('\n' + text + ' running...\n')

    final_y = cnn(x)[0]#, xSize, downsampling = downsampling
    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=final_y))
    
    correct_prediction = tf.equal(tf.argmax(final_y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
 
    batch_size = tfFLAGS.batch_size
    train_size = mnist.train.images.shape[0]
    total_batch_size = int(train_size / batch_size)
    
    keep_prob = tf.placeholder(tf.float32)
    global_step = tf.Variable(0)
    learning_rate = tf.train.exponential_decay(1e-4,  global_step * batch_size, train_size, 0.95, staircase=True)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy, global_step = global_step)
        
    sess.run(tf.global_variables_initializer())
    
    for epoch in range(iterations):
        mnist.train.shuffle()
        for batchCount in range(total_batch_size):
            batch = mnist.train.next_batch(batch_size)
            start_time = time.time()
            sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
            if epoch > 0 and epoch % tfFLAGS.log_frequency == 0 and batchCount == total_batch_size-1:
                feed_dict = {x:batch[0], y_: batch[1], keep_prob: 1.0}
                train_accuracy = accuracy.eval(feed_dict = feed_dict)
                
                duration = time.time() - start_time
                num_examples_per_step = tfFLAGS.batch_size * tfFLAGS.num_gpus
                examples_per_sec = num_examples_per_step / duration
                sec_per_batch = duration / tfFLAGS.num_gpus

                print_('Epoch %d, (%.2f batch accuracy; %.1f examples/sec; %.3f sec/batch) by %s' % 
                                                         (epoch, train_accuracy, examples_per_sec, sec_per_batch, nowStr()))

   

    feed_dict = {x: mnist.train.images, y_: mnist.train.labels, keep_prob: 1.0}
    feed_dict = {x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}

    print_("\nThe test accuracy = %g" % accuracy.eval(feed_dict = feed_dict))
    print_(' ')
