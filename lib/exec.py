import os
import pwd

def current_user():
    return pwd.getpwuid(os.getuid()).pw_name

def sudo(cmd):
    return subprocess.Popen(['sudo'] + cmd, shell=True,
                       stderr = subprocess.PIPE,
                       stdout = subprocess.PIPE,
                       stdin = subprocess.PIPE)

def exec(cmd):
    return subprocess.Popen(['sudo'] + cmd, shell=True,
                       stderr = subprocess.PIPE,
                       stdout = subprocess.PIPE,
                       stdin = subprocess.PIPE)
