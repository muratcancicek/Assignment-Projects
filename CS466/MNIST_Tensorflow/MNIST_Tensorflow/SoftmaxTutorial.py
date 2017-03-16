from VersionHandler import *
import tensorflow as tf

def runSoftmax(mnist, x, y_):
    print('\nSoftmaxTutorial running...')
    W = tf.Variable(tf.zeros([784, 10]))
    b = tf.Variable(tf.zeros([10]))
    y = tf.matmul(x, W) + b
    # The raw formulation of cross-entropy,
    #
    #   tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(tf.nn.softmax(y)),
    #                                 reduction_indices=[1]))
    #
    # can be numerically unstable.
    #
    # So here we use tf.nn.softmax_cross_entropy_with_logits on the raw
    # outputs of 'y', and then average across the batch.
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()
    # Train
    for _ in range(1000):
        batch_xs, batch_ys = mnist.train.next_batch(100)
        #batch_xs = np.reshape(batch_xs, (-1, 784))
        #batch_ys = np.reshape(batch_ys, (-1, 10))
        sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    # Test trained model
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    accuracyValue = sess.run(accuracy, feed_dict={x: mnist.test.images,
                                        y_: mnist.test.labels})
    prnt('The accuracy of sofmax on local files = ', accuracyValue)
    print(' ')
    #a = True
    #if a:#__name__ == '__main__':
    #    parser = argparse.ArgumentParser()
    #    parser.add_argument('--data_dir', type=str, default='/tmp/tensorflow/mnist/input_data',
    #                        help='Directory for storing input data')
    #    FLAGS, unparsed = parser.parse_known_args()
    #    tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)