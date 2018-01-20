# RYU-Firewall
Python script to implement RYU controller for forwarding and firewall functionality

Steps:
1. Before initializing Floodlight, edit the file - /home/sdn/floodlight/src/main/resources/ floodlightdefault.properties file and remove the line - net.floodlightcontroller.forwarding.Forwarding,\
2. The above step is to disable the controller's ability to install reactive forwarding rules on the switch when the switch receives packets from the hosts. Now only proactive forwarding rules can be installed by the controller else the packets will be dropped and no communication can happen.
3. Use mininet to create testing topology. Initialize the controller IP also - Command: sudo mn --topo=linear,2,2 --mac --controller=remote,ip=192.168.56.101 --switch=ovsk,protocols=OpenFlow13
4. Execute the python script to start a Flask GUI with various options to add forwarding rules and firewall options.
