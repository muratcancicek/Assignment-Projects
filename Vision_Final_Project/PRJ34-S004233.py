#   Muratcan Cicek Department of Computer Science                           #
#   CS 423/523 Computer Vision Fall 2016 [Project 3-4] @Ozyegin_University  # 

import cv2
import cPickle
import numpy as np
from matplotlib import pyplot as plt
#from kmaens import *
 
def unpickle(file):
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict


dict1 = unpickle('data_batch_1')
test_batch = unpickle('test_batch')
#print dict1.keys()
#print dict1['data'].size
#print dict1['data'][0]
#print dict1['labels'][0]
sample = dict1['data'][0]
print sample[0]


from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

m = 1000 
data = dict1['data'][:m]

data = scale(data)
n_samples, n_features = data.shape
labels = dict1['labels'][:m]
n_digits = 10

sample_size = 100

#print("n_categories: %d, \t n_samples %d, \t n_features %d"
#      % (n_digits, n_samples, n_features))


print(79 * '_')
#print('% 9s' % 'init'
#      '    time  inertia    accuracy    homo   compl  v-meas     ARI AMI  silhouette')


def bench_k_means(estimator, name, data, test_batch):
    t0 = time()
    estimator.fit(data)
    labels2 = estimator.predict(test_batch['data'])
    print 'accuracy', metrics.accuracy_score(labels2, test_batch['labels'])
    #print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
    #      % (name, (time() - t0), estimator.inertia_,
    #         metrics.accuracy_score(labels, estimator.labels_),
    #         metrics.homogeneity_score(labels, estimator.labels_),
    #         metrics.completeness_score(labels, estimator.labels_),
    #         metrics.v_measure_score(labels, estimator.labels_),
    #         metrics.adjusted_rand_score(labels, estimator.labels_),
    #         metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
    #         metrics.silhouette_score(data, estimator.labels_,
    #                                  metric='euclidean',
    #                                  sample_size=sample_size)))

#bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
#              name="k-means++", data=data)

bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),
              name="random", data=data, test_batch = test_batch)

# in this case the seeding of the centers is deterministic, hence we run the
# kmeans algorithm only once with n_init=1
pca = PCA(n_components=n_digits).fit(data)
bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),
              name="PCA-based",
              data=data, test_batch = test_batch)
#print(79 * '_')

#reduced_data = PCA(n_components=2).fit_transform(data)
#kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
#kmeans.fit(reduced_data)

## Step size of the mesh. Decrease to increase the quality of the VQ.
#h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

## Plot the decision boundary. For that, we will assign a color to each
#x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
#y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
#xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

## Obtain labels for each point in mesh. Use last trained model.
#Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

## Put the result into a color plot
#Z = Z.reshape(xx.shape)
#plt.figure(1)
#plt.clf()
#plt.imshow(Z, interpolation='nearest',
#           extent=(xx.min(), xx.max(), yy.min(), yy.max()),
#           cmap=plt.cm.Paired,
#           aspect='auto', origin='lower')

#plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
## Plot the centroids as a white X
#centroids = kmeans.cluster_centers_
##plt.scatter(centroids[:, 0], centroids[:, 1],
##            marker='x', s=169, linewidths=3,
##            color='w', zorder=10)
#plt.title('K-means clustering on the CIFAR10 dataset (PCA-reduced data)\n')
#plt.xlim(x_min, x_max)
#plt.ylim(y_min, y_max)
#plt.xticks(())
#plt.yticks(())
#plt.show()
print 'DONE'