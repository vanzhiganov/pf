# installation

1. create file: interface.conf
2. interface.conf file must contain external ethernet port name, for example: eth0
3. create folder for pid files `mkdir /var/run/container/pf`

# using

## run pf rule

1. create file with pf rule

`$ echo "<external port> <destination ip> <destination port>" > <external port>.rule`

for example

`$ echo "9100 10.10.10.1 22" > 9100.rule`

2. run pf

`$ python pf.py <external port number>`

## kill running pf rule

`$ python pfkill.py <external port number>`
