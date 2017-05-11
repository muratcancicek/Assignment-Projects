from cifar10 import * 
import tfFLAGS 

def activation_summary(x):
  tensor_name = re.sub('%s_[0-9]*/' % tfFLAGS.TOWER_NAME, '', x.op.name)
  tf.summary.histogram(tensor_name + '/activations', x)
  tf.summary.scalar(tensor_name + '/sparsity', tf.nn.zero_fraction(x))

def variable_on_cpu(name, shape, initializer):
  with tf.device('/cpu:0'):
    dtype = tf.float16 if tfFLAGS.use_fp16 else tf.float32
    var = tf.get_variable(name, shape, initializer=initializer, dtype=dtype)
  return var

def variable_with_weight_decay(name, shape, stddev, wd):
  dtype = tf.float16 if tfFLAGS.use_fp16 else tf.float32
  var = variable_on_cpu(name, shape, tf.truncated_normal_initializer(stddev=stddev, dtype=dtype))
  if wd is not None:
    weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')
    tf.add_to_collection('losses', weight_decay)
  return var

# Architecture of model
conv1Size = 5; conv1Out = 8; conv1Shape = [conv1Size, conv1Size, 3, conv1Out]
conv2Size = 5; conv2Shape = [conv2Size, conv2Size, conv1Out, 10]

pool1S = 4; pool1ksize=[1, pool1S, pool1S, 1]; pool1St = 2; pool1strides=[1, pool1St, pool1St, 1]; pool1padding='SAME'
pool2S = 3; pool2ksize=[1, pool2S, pool2S, 1]; pool2St = 2; pool2strides=[1, pool2St, pool2St, 1]; pool2padding='SAME'

local3InputDepth = 64 * conv2Shape[-1]; local3OutputDepth = local3InputDepth
local4InputDepth = local3OutputDepth; local4OutputDepth = 16
softmax_linearInput = local4OutputDepth
def summarizeModel():
    print_('Summary of Network 1:')
    print_('conv1Shape:', conv1Shape)
    print_('pool1ksize:', pool1ksize, ' | pool1strides:', pool1strides, ' | pool1padding:', pool1padding)
    print_('conv2Shape:', conv2Shape)
    print_('pool2ksize:', pool2ksize, ' | pool2strides:', pool2strides, ' | pool2padding:', pool2padding)
    print_('local3InputDepth:', local3InputDepth, ' | local3OutputDepth:', local3OutputDepth)
    print_('local4InputDepth:', local4InputDepth, ' | local4OutputDepth:', local4OutputDepth)
    print_('softmax_linearInput:', softmax_linearInput)
    print_()
    numParamConv1 = (conv1Shape[0] * conv1Shape[1] * conv1Shape[2]) * conv1Shape[-1]
    print_('Number of hidden parameters of conv1:', numParamConv1)
    print_('Number of hidden parameters of conv1Biases:', conv1Shape[-1]) 
    numParamConv1 += conv1Shape[-1]
    #print_('Number of hidden parameters of norm:', numParamConv1 / pool1S**1)
    numParamConv2 = (conv2Shape[0] * conv2Shape[1] * conv2Shape[2]) * conv2Shape[-1]
    print_('Number of hidden parameters of conv2:', numParamConv2)
    print_('Number of hidden parameters of conv2Biases:', conv2Shape[-1]) 
    numParamConv2 += conv2Shape[-1]
    numParamLocal3 = (local3InputDepth) * local3OutputDepth
    print_('Number of hidden parameters of local3:', numParamLocal3)
    print_('Number of hidden parameters of local3Biases:', local3OutputDepth)
    numParamLocal3 += local3OutputDepth
    numParamLocal4 = (local4InputDepth) * local4OutputDepth
    print_('Number of hidden parameters of local4:', numParamLocal4)
    print_('Number of hidden parameters of local4Biases:', local4OutputDepth)
    numParamLocal4 += local4OutputDepth
    numParamsoftmax = (softmax_linearInput) * tfFLAGS.NUM_CLASSES
    print_('Number of hidden parameters of softmax:', numParamsoftmax)
    print_('Number of hidden parameters of softmaxBiases:', tfFLAGS.NUM_CLASSES)
    numParamsoftmax += tfFLAGS.NUM_CLASSES
    print_('Total number of hidden parameters:', numParamConv1 + numParamConv2 + numParamLocal3 + numParamLocal4 + numParamsoftmax)

def inference(images):
    with tf.variable_scope('network2') as scope:
        # conv1
        with tf.variable_scope('conv1') as scope:
            kernel = variable_with_weight_decay('weights', shape=conv1Shape, stddev=5e-2, wd=0.0)
            conv = tf.nn.conv2d(images, kernel, [1, 1, 1, 1], padding='SAME')
            biases = variable_on_cpu('biases', [conv1Shape[-1]], tf.constant_initializer(0.0))
            pre_activation = tf.nn.bias_add(conv, biases)
            conv1 = tf.nn.relu(pre_activation, name=scope.name)
            activation_summary(conv1)
        # pool1
        pool1 = tf.nn.max_pool(conv1, ksize=pool1ksize, strides=pool1strides, padding=pool1padding, name='pool1')
        # norm
        norm = tf.nn.lrn(pool1, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75, name='norm')

        # conv2
        with tf.variable_scope('conv2') as scope:
            kernel = variable_with_weight_decay('weights', shape=conv2Shape, stddev=5e-2, wd=0.0)
            conv = tf.nn.conv2d(norm, kernel, [1, 1, 1, 1], padding='SAME')
            biases = variable_on_cpu('biases', [conv2Shape[-1]], tf.constant_initializer(0.1))
            pre_activation = tf.nn.bias_add(conv, biases)
            conv2 = tf.nn.relu(pre_activation, name=scope.name)
            activation_summary(conv2)

        # norm2
        norm2 = tf.nn.lrn(conv2, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75, name='norm2')
        # pool2
        pool2 = tf.nn.max_pool(norm2, ksize=pool2ksize, strides=pool2strides, padding=pool2padding, name='pool2')

        # local3
        with tf.variable_scope('local3') as scope:
            # Move everything into depth so we can perform a single matrix multiply.
            reshape = tf.reshape(pool2, [tfFLAGS.batch_size, -1])
            local3InputDepth = reshape.get_shape()[1].value
            fc1_weights = variable_with_weight_decay('weights', shape=[local3InputDepth, local3OutputDepth], stddev=0.04, wd=0.004)
            fc1_biases = variable_on_cpu('biases', [local3OutputDepth], tf.constant_initializer(0.1))
            local3 = tf.nn.relu(tf.matmul(reshape, fc1_weights) + fc1_biases, name=scope.name)        
            activation_summary(local3)

        # local4
        with tf.variable_scope('local4') as scope:
            fc2_weights = variable_with_weight_decay('weights', shape=[local3OutputDepth, local4OutputDepth], stddev=0.04, wd=0.004)
            fc2_biases = variable_on_cpu('biases', [local4OutputDepth], tf.constant_initializer(0.1))
            local4 = tf.nn.relu(tf.matmul(local3, fc2_weights) + fc2_biases, name=scope.name)
            activation_summary(local4)
        
        with tf.variable_scope('softmax_linear') as scope:
            weights = variable_with_weight_decay('weights', [softmax_linearInput, tfFLAGS.NUM_CLASSES], stddev=1/192.0, wd=0.0)
            biases = variable_on_cpu('biases', [tfFLAGS.NUM_CLASSES], tf.constant_initializer(0.0))
            softmax_linear = tf.add(tf.matmul(local4, weights), biases, name=scope.name)
            activation_summary(softmax_linear)

    return softmax_linear, fc1_weights, fc1_biases, fc2_weights, fc2_biases
