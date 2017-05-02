from cifar10_train import main as run_cifar10_train
from cifar10_multi_gpu_train import main as run_cifar10_multi_gpu_train
from cifar10_eval import main as run_cifar10_eval, tf
from PythonVersionHandler import *
from paths import *

def printSeparater():
    for n in range(3):
        print_('#' * 88)
        
def main(method = None):
    printSeparater()
    print_('%s:' % nowStr(), 'Running on', COMPUTERNAME + '...')
    
    if method == None:
      #   run_cifar10_multi_gpu_train()
        run_cifar10_train()
        run_cifar10_eval()
    else:
        method()

    print_('%s:' % nowStr(), 'DONE')
    printSeparater()

    if COMPUTERNAME == 'MSI' or COMPUTERNAME == 'LM-IST-00UBFVH8':
        sys.exit() 

if __name__ == "__main__":
    main()