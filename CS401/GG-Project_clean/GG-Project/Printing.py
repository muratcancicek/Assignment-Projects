#import sys
#if sys.version_info[0] == 3:
#    import colorama
#    colorama.init()
class bcolors:
    PINK = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    GRAY = '\033[1;30m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEFAULT = '\033[0m'

def pink(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.PINK + s + bcolors.DEFAULT

def cyan(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.CYAN + s + bcolors.DEFAULT

def darkCyan(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.DARKCYAN + s + bcolors.DEFAULT

def gray(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.GRAY + s + bcolors.DEFAULT

def blue(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.BLUE + s + bcolors.DEFAULT

def green(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.GREEN + s + bcolors.DEFAULT

def yellow(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.YELLOW + s + bcolors.DEFAULT

def red(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.RED + s + bcolors.DEFAULT

def bold(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.BOLD + s + bcolors.DEFAULT

def underline(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.UNDERLINE + s + bcolors.DEFAULT
