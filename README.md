# RYU-Firewall
Python script to implement RYU controller for forwarding and firewall functionality

Steps:
1. Use mininet to create testing topology. Initialize the controller IP also - Command: sudo mn --topo=linear,2,2 --mac --controller=remote,ip=192.168.56.101 --switch=ovsk,protocols=OpenFlow13
2. Execute the python script to start a Flask GUI with various options to add forwarding rules and firewall options.
