# BeagleCom
BeagleCom is based around the concept of a centralized tracker and an associated swarm of peers able to share file and communicate.

```
python3 sendfile.py -i <localhost> -p <port> -f <file path>
```
To send and receive files and folders globally, the receiver run NGROK
```
./ngrok tcp <receiver port>
python3 receiver.py
```
To use launch the IRC client
```
python3 irc_client.py <nusername> <channeltojoin>  
```

