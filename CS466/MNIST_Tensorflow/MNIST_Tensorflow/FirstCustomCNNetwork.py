from PythonVersionHandler import *
import tensorflow as tf
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

def buildBiasedLayers(input, shape, transaction, activationFunction = lambda x: x): # activationFunction = None 
    weight = weight_variable(shape)
    bias = bias_variable([shape[-1]])
    output = activationFunction(transaction(input, weight) + bias)
    #print_('Biased Output shape:', output.shape)
    return output

def buildConvReluMaxPoolLayers(input, patch, inputChannel, outputChannel, poolSize = 2):
    shape = [patch, patch, inputChannel, outputChannel]
    h_conv = buildBiasedLayers(input, shape, conv2d, tf.nn.relu)
    output = max_pool(h_conv, n = poolSize)
    print_('MaxPool Output shape:', output.shape)
    return output
    
def buildFullyConnectedLayers(input, inputChannel, outputChannel):
    shape = [inputChannel, outputChannel]
    flat_input = tf.reshape(input, [-1, shape[0]])
    output = buildBiasedLayers(flat_input, shape, tf.matmul)
    print_('Fully Connected Output shape:', output.shape)
    return output
     
def runCFirstCustomCNN(mnist, x, y_, xSize = 784, iterations = 1000, downsampling = False):
    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    print('\nFirst Custom CNN running...')

    initialSize = int(math.sqrt(xSize))
    x_image = tf.reshape(x, [-1, initialSize, initialSize, 1])
    downsamplingSize = 1
    if downsampling:
        outputBridge1 = 1; downsamplingSize = 2; poolSize1 = downsamplingSize
        h_pool1 = downsample(x_image, downsamplingSize)
    else:
        outputBridge1 = 64; poolSize1 = 2
        h_pool1 = buildConvReluMaxPoolLayers(x_image, 5, 1, outputBridge1, poolSize1) 
    
    #outputBridge1 = 64; poolSize1 = 2
    #h_pool1 = buildConvReluMaxPoolLayers(h_pool1, 5, 1, outputBridge1, poolSize1) 

    outputBridge2 = 64; poolSize2 = 2
    h_pool2 = buildConvReluMaxPoolLayers(h_pool1, 5, outputBridge1, outputBridge2, poolSize2)
    
    outputBridge3 = 32
    finalSize = int(int(int(initialSize / poolSize1) / poolSize2 ) / downsamplingSize)
   
    h_fc1 = buildFullyConnectedLayers(h_pool2, finalSize * finalSize * outputBridge2, outputBridge3)

    y_conv = buildFullyConnectedLayers(h_fc1, outputBridge3, 10)

    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
    
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
 
    global_step = tf.Variable(0)

    starter_learning_rate = 1e-4 #0.9#, trainable=False
    learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step,
                                                   1, 0.9999, staircase=True)
    train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy, global_step = global_step)
        
    BATCH_SIZE = 50
    keep_prob = tf.placeholder(tf.float32)
    sess.run(tf.global_variables_initializer())
    for batchCount in range(iterations):
        batch = mnist.train.next_batch(BATCH_SIZE)
        if batchCount > 0 and batchCount % 100 == 0:
            feed_dict = {x:batch[0], y_: batch[1], keep_prob: 1.0}
            train_accuracy = accuracy.eval(feed_dict = feed_dict)
            print("step %d, training accuracy %.2f" % (batchCount, train_accuracy))
   
        sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    feed_dict = {x: mnist.train.images, y_: mnist.train.labels, keep_prob: 1.0}
    print("The train accuracy of CNNTutorial on local files = %g" % accuracy.eval(feed_dict = feed_dict))
    print(' ')


    feed_dict = {x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}
    print("The test accuracy of CNNTutorial on local files = %g" % accuracy.eval(feed_dict = feed_dict))
    print(' ')
