#CODE

#Generate root password
import getpass
import random
import string
password = ''.join(random.choice(string.ascii_letters + string.digits)
                   for i in range(20))

#Download ngrok
! wget - q - c - nc https: // bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
! unzip - qq - n ngrok-stable-linux-amd64.zip
#Setup sshd
! apt-get install - qq - o = Dpkg: : Use-Pty = 0 openssh-server pwgen > /dev/null
#Set root password
! echo root: $password | chpasswd
! mkdir - p / var/run/sshd
! echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
! echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
! echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc
! echo "export LD_LIBRARY_PATH" >> /root/.bashrc

#Run sshd
get_ipython().system_raw('/usr/sbin/sshd -D &')

#Ask token
print("Copy authtoken from https://dashboard.ngrok.com/auth")
authtoken = getpass.getpass()

#Create tunnel
get_ipython().system_raw('./ngrok authtoken $authtoken && ./ngrok tcp 22 &')
#Print root password
print("Root password: {}".format(password))
#Get public address
! curl - s http: // localhost: 4040/api/tunnels | python3 - c \
    "import sys, json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"