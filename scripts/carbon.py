from socket import socket
import sys

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

sock = socket()
try:
    sock.connect((CARBON_SERVER, CARBON_PORT))
except:
    print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?"\
          % {'server': CARBON_SERVER, 'port': CARBON_PORT}
    sys.exit(1)


def send(lines):
    # all lines must end in a newline
    message = '\n'.join(lines) + '\n'
    print "sending message\n"
    print '-' * 80
    print message
    print
    sock.sendall(message)
