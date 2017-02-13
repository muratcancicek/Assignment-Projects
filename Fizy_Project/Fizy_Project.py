#hostname = raw_input('hostname: ')
#username = raw_input('username: ')
#password = getpass.getpass('password: ')
hostname = '127.0.0.1'
username = 'm'
password = ' '
#import base64
#import paramiko
##key = paramiko.RSAKey(data=base64.b64decode(b'AAA')) # 'AAAAS'
#client = paramiko.SSHClient()
##client.get_host_keys().add(hostname, username, key)
#client.load_system_host_keys()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#client.connect(hostname, username=username, password=password)
#stdin, stdout, stderr = client.exec_command('ls')
#for line in stdout:
#    print('... ' + line.strip('\n'))
#client.close()

from pexpect import pxssh

try:                                                            
    s = pxssh.pxssh()
    s.login (hostname, username, password)
    s.sendline ('uptime')   # run a command
    s.prompt()             # match the prompt
    print s.before          # print everything before the prompt.
    s.sendline ('ls -l')
    s.prompt()
    print s.before
    s.sendline ('df')
    s.prompt()
    print s.before
    s.logout()
except pxssh.ExceptionPxssh, e:
    print "pxssh failed on login."
    print str(e)