# BeagleCom
BeagleCom is a project with the aim to equip the BeagleBone with easy-to-use and accessible communication tools. A file sharing system and a IRC client capable to connect to any public channel.

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
python3 irc_client.py <username> <channeltojoin>  
```

More information are available on the Wiki: <https://elinux.org/ECE_434_BeagleCom>
Video demo: <https://youtu.be/C6mogTZ1gCY>

Beagle login backgroung : Photo by Oliver on Unsplash
