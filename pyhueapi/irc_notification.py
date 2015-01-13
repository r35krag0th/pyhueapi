import socket
from time import sleep

def send_preset(name, room, channel="#automation"):
    if room == 'all':
        room = 'all rooms'

    prefixed_message = "[@]11<[@]15Preset[@]11> [@]08[!]%s[!] [@]00has been run in [@]09%s." % (name, room)
    send(prefixed_message)

def send(message, channel="#automation"):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('bots.r35.private', 9200))
    client.send("%s [@]02([@]15PyHueApi[@]02) [@]00%s\r\n" % (channel, message))

    # Keep the socket from closing too fast
    sleep(0.5)
    client.shutdown(socket.SHUT_RDWR)
    client.close()
