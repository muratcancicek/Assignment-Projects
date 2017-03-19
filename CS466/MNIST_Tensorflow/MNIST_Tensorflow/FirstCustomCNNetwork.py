from PythonVersionHandler import *
import tensorflow as tf
import math

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

def runCFirstCustomCNN(mnist, x, y_, xSize = 784, iterations = 1000):
    print('\nFirst Custom CNN running...')
    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    patch, inputChannels, outputChannels = 5, 1, 32
    W_conv1 = weight_variable([patch, patch, inputChannels, outputChannels])
    b_conv1 = bias_variable([outputChannels])

    n = int(math.sqrt(xSize))
    x_image = tf.reshape(x, [-1,n,n,1])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)
    
    patch, inputChannels, outputChannels = 5, 1, 128
    W_conv2 = weight_variable([patch, patch, inputChannels, outputChannels])
    b_conv2 = bias_variable([outputChannels])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)
    W_fc1 = weight_variable([8 * 2 * 64, 2048])
    b_fc1 = bias_variable([2048])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 8*2*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    W_fc2 = weight_variable([2048, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    sess.run(tf.global_variables_initializer())

    for i in range(iterations):
      batch = mnist.train.next_batch(50)
      #print_(batch[0].shape)
      #print_(batch[1].shape)
      if i%100 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x:batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g"%(i, train_accuracy))
      train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

    print("The accuracy of CNNTutorial on local files = %g"%accuracy.eval(feed_dict={
        x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))
    print(' ')
