import essentia 
import essentia.standard as ess
from matplotlib.pyplot import plot, show, figure, imshow

#print essentia
# we start by instantiating the audio loader:
loader = ess.MonoLoader(filename='data/mp3s/HotlineBling.mp3')

# and then we actually perform the loading:
audio = loader()
# pylab contains the plot() function, as well as figure, etc... (same names as Matlab)
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15, 6) # set plot sizes to something larger than default

plot(audio[1*44100:2*44100])
plt.title("This is how the 2nd second of this audio looks like:")
plt.savefig('data/plots/HotlineBling_testplot.png')