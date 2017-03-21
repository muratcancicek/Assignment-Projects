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

def buildBiasedLayers(input, shape, transaction = conv2d, activationFunction = lambda x: x): # activationFunction = None 
    weight = weight_variable(shape)
    bias = bias_variable([shape[-1]])
    output = activationFunction(transaction(input, weight) + bias)
    #print_('Biased Output shape:', output.shape)
    return output

def buildConvReluMaxPoolLayers(input, patch, inputChannel, outputChannel, poolSize = 2):
    shape = [patch, patch, inputChannel, outputChannel]
    h_conv = buildBiasedLayers(input, shape, conv2d, tf.nn.relu)
    output = max_pool(h_conv, n = poolSize)
    #print_('MaxPool Output shape:', output.shape)
    return output
     
def dropoutLayer(x):
    keep_prob = tf.placeholder(tf.float32)
    return tf.nn.dropout(x, keep_prob)

def buildFullyConnectedLayers(input, inputChannel, outputChannel):
    shape = [inputChannel, outputChannel]
    flat_input = tf.reshape(input, [-1, shape[0]])
    output = buildBiasedLayers(flat_input, shape, tf.matmul)
    #print_('Fully Connected Output shape:', output.shape)
    return output
     
def inputLayer(x, xSize, downsampling = False, poolSize = 2, patch = 5, outputBridge = 196):
    initialSize = int(math.sqrt(xSize))
    input = tf.reshape(x, [-1, initialSize, initialSize, 1])
    if downsampling:
        output = downsample(input, poolSize)
        shape = [patch, patch, 1, outputBridge]
        #output = buildBiasedLayers(input, shape, conv2d, tf.nn.relu)
        outputBridge = 1
        #output = buildConvReluMaxPoolLayers(output, patch, 1, outputBridge, poolSize) 
    else:
        output = buildConvReluMaxPoolLayers(input, patch, 1, outputBridge, poolSize) 
        #output = max_pool(x_image, poolSize) 
    n = int(initialSize/poolSize)
    #print_('Output:', output, outputBridge, n)
    return output, outputBridge, n

def hiddenLayer1(input, inputBridge, n, patch = 5, poolSize = 2, outputBridge = 64):
    output = buildConvReluMaxPoolLayers(input, patch, inputBridge, outputBridge, poolSize) 
    #output = buildFullyConnectedLayers(input, n * n * inputBridge, outputBridge) 
    n = int(n/poolSize)
    #print_('Output:', output, outputBridge, n)
    return output, outputBridge, n

def hiddenLayer2(input, inputBridge, n, outputBridge = 1024):
    output = buildFullyConnectedLayers(input, n * n * inputBridge, outputBridge) 
    n = 1
    return output, outputBridge, n

def lastLayer(input, inputBridge, n):
    output = dropoutLayer(input)
    output = buildFullyConnectedLayers(input, n * n * inputBridge, 10)
    return output

def firstCNN(x, xSize, downsampling = False):

    output, outputBridge, n = inputLayer(x, xSize, downsampling = downsampling,
                                         poolSize = 2, patch = 5, outputBridge = 32)

    output, outputBridge, n = hiddenLayer1(output, outputBridge, n, 
                                           poolSize = 2, patch = 5, outputBridge = 64)

    output, outputBridge, n = hiddenLayer2(output, outputBridge, n, outputBridge = 512)

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

    final_y = cnn(x, xSize, downsampling = downsampling)

    cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=final_y))
    
    correct_prediction = tf.equal(tf.argmax(final_y,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
 
    global_step = tf.Variable(0)

    starter_learning_rate = 1e-4 #0.9#, trainable=Falselearning_rate
    learning_rate = tf.train.exponential_decay(starter_learning_rate, global_step,
                                                   1, 0.9999, staircase=True)
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy, global_step = global_step)
        
    BATCH_SIZE = 200
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
    #print("The train accuracy of CNNTutorial on local files = %g" % accuracy.eval(feed_dict = feed_dict))
    #print(' ')

    #for i in xrange(10):
    #testSet = mnist.test.next_batch(50)
    #print("test accuracy %g"%accuracy.eval(feed_dict={ x: testSet[0], y_: testSet[1], keep_prob: 1.0}))
    feed_dict = {x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}
    print_("\nThe test accuracy = %g" % accuracy.eval(feed_dict = feed_dict))
    print_(' ')
