class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def header(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.HEADER + s + bcolors.ENDC

def blue(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.OKBLUE + s + bcolors.ENDC

def green(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.OKGREEN + s + bcolors.ENDC

def yellow(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.WARNING + s + bcolors.ENDC

def red(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.FAIL + s + bcolors.ENDC

def bold(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.BOLD + s + bcolors.ENDC

def underline(s):
    if not isinstance(s, str): s = str(s)
    return bcolors.UNDERLINE + s + bcolors.ENDC
