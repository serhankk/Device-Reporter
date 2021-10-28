# Imports
from prettytable import PrettyTable
import socket, subprocess, os, requests, CONFIG

def send_message(text):
    try:
        requests.post('https://slack.com/api/chat.postMessage', {
        'token': CONFIG.SLACK_TOKEN,
        'channel': CONFIG.SLACK_CHANNEL_INFO,
        'text': text,
        'username': CONFIG.SLACK_BOT_NAME,
})
    except Exception as e:
        print(e)

def get_hostname():
    try:
        return socket.gethostname()
    except:
        pass

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
    try:
        output = str(subprocess.check_output(['iwgetid']))
        network= output.split('"')[1]
        return network
    except:
        pass

def get_using_interface():
    try:
        output = str(subprocess.check_output(['iwgetid']))
        network = output.split(' ')[0]
        return network
    except:
        pass

def get_device_uptime():
    try:
        t = os.popen('uptime -p').read()[:-1]
        t = [f'{x.capitalize()} ' for x in t.split(' ')]
        t = ''.join(t).rstrip()
        return t
    except:
        pass

def get_ram_usage():
    try:
        total_m = os.popen('free -h').readlines()[1].split()[1]
        used_m= os.popen('free -h').readlines()[1].split()[2]
        return f'{used_m} of {total_m}'
    except:
        pass
hostname = get_hostname()
local_ip = get_local_ip()
wifi = get_connected_network()
interface = get_using_interface()
uptime = get_device_uptime()
ram = get_ram_usage()

information = '''HOSTNAME: "{}"
LOCAL IP: "{}"
CONNECTED NETWORK: "{}"
USING NETWORK INTERFACE: "{}"
DEVICE UPTIME: "{}"
RAM USAGE: "{}"'''.format(hostname, local_ip, wifi, interface, uptime, ram)

table = PrettyTable(['Hostname', 'Local IP', 'Wi-Fi', 'Interface', 'Uptime', 'RAM'])
data = ([hostname, local_ip, wifi, interface, uptime, ram])
table.add_row(data)


print(table)
send_message(information)
