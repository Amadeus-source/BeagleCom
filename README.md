# BeagleCom
BeagleCom is a project with the aim to equip the BeagleBone with easy-to-use and accessible communication tools. A file sharing system and a IRC client capable.

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

