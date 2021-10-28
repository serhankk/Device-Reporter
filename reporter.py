# Imports
import socket, subprocess, os

def introduction(text):
    print('-' * 60)
    print(text.center(60))
    print('-' * 60)

def get_hostname():
    return socket.gethostname()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_connected_network():
    output = str(subprocess.check_output(['iwgetid']))
    network= output.split('"')[1]
    return network

def get_using_interface():
    output = str(subprocess.check_output(['iwgetid']))
    network = output.split(' ')[0]
    return network

def get_device_uptime():
    t = os.popen('uptime -p').read()[:-1]
    t = [f'{x.capitalize()} ' for x in t.split(' ')]
    t = ''.join(t).rstrip()
    return t

def get_ram_usage():
    total_m = os.popen('free -h').readlines()[1].split()[1]
    used_m= os.popen('free -h').readlines()[1].split()[2]
    return f'{used_m} of {total_m}'


information = '''HOSTNAME: "{}"
LOCAL IP: "{}"
CONNECTED NETWORK: "{}"
USING NETWORK INTERFACE: "{}"
DEVICE UPTIME: "{}"
RAM USAGE: "{}"
'''

introduction('DEVICE INFORMER')
print(information.format(get_hostname(), get_local_ip(), get_connected_network(), get_using_interface(), get_device_uptime(), get_ram_usage()))