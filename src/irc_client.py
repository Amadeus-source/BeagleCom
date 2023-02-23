#!/usr/bin/env python3
import socket
import threading
import sys
import time
import json
import Adafruit_BBIO.GPIO as GPIO

LED = "P9_12"
f = open('../config.json', 'r')
data = json.load(f)

def usage():
    print("IRC Client \n")
    print("$ ./irc_client.py USERNAME CHANNEL\n")
    print("where: USERNAME - your username, CHANNEL - channel you'd like to join (eg. channelname or #channelname)")


def channel(channel):
    if channel.startswith("#") == False:
        return "#" + channel
    return channel

# helper function used as thread target
def print_response():
    resp = client.get_response().decode()
    if "PING" in resp:
            client.send_cmd("PONG", ":" + resp.split(":")[1])
    if resp:
        msg = resp.strip().split(":")
        decoded = "<{}> {} \n".format(msg[1].split("!")[0], msg[2].strip())
        print(decoded)
        with open("../src/logs.txt", "a") as outfile:
                outfile.write(decoded)
                toggle()

#toggle LED
def toggle():
        GPIO.setup(LED, GPIO.OUT)
        GPIO.output(LED, 1)
        time.sleep(1)
        GPIO.output(LED, 0)
        time.sleep(1)

class IRCSimpleClient:

    def __init__(self, username, channel, server="chat.freenode.net", port=6667):
        self.username = username
        self.server = server
        self.port = port
        self.channel = channel

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server, self.port))

    def get_response(self):
        return self.conn.recv(4096)

    def send_cmd(self, cmd, message):
        command = "{} {}\r\n".format(cmd, message)
        self.conn.send(command.encode())

    def send_message_to_channel(self, message):
        command = "PRIVMSG {}".format(self.channel)
        message = ":" + message
        self.send_cmd(command, message)

    def join_channel(self):
        cmd = "JOIN"
        channel = self.channel
        self.send_cmd(cmd, channel)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        exit(0)
    else:
        username = sys.argv[1]
        channel = channel(sys.argv[2])

    cmd = ""
    joined = False
    client = IRCSimpleClient(username, channel)
    client.connect()

    while(joined == False):
        resp = client.get_response().decode()
        print(resp.strip())
        time.sleep(1)
        if "Looking up" in resp:
            client.send_cmd("NICK", username)
            client.send_cmd(
                "USER", "{} * * :{}".format(username, username))

        # we're accepted, now let's join the channel!
        if "376" in resp:
            client.join_channel()

        # username already in use? try to use username with _
        if "433" in resp:
            username = "_" + username
            client.send_cmd("NICK", username)
            client.send_cmd(
                "USER", "{} * * :{}".format(username, username))

        # if PING send PONG with name of the server
        if "PING" in resp:
            client.send_cmd("PONG", ":" + resp.split(":")[1])

        # we've joined
        if "366" in resp:
            joined = True

        else:
            client.send_cmd("NICK", username)
            client.send_cmd(
                "USER", "{} * * :{}".format(username, username))


    while(cmd != "/quit"):
        try:
            cmd = input("\n<{}> ".format(username)).strip()
            with open("../src/logs.txt", "a") as outfile:
                outfile.write("<{}> {} \n".format(username, cmd))
            if cmd == "/quit":
                client.send_cmd("QUIT", "Good bye!")
            client.send_message_to_channel(cmd)

            # socket conn.receive blocks the program until a response is received
            # to prevent blocking program execution, receive should be threaded
            response_thread = threading.Thread(target=print_response)
            response_thread.daemon = True
            response_thread.start()
        
        except KeyboardInterrupt:
            print("Closing and Exiting...")
            client.send_cmd("QUIT", "Good bye!")