README

NAME : SRIRAGH KARAT


DESCRIPTION OF CODE FILE:

There are 5 different code files in this project:

1. of_tutorial.py - In this code file we implemented the act_like_switch function and verified behavior of a switch.

2. mytopo1.py - In this code the topology of Part A of the project was implemented. The topology consisted of three hosts and a
switch. The switch was connected to each of the host. The hosts had the following IP addresses:

Host 1 - 10.0.1.100/24

Host 2 - 10.0.2.100/24

Host 3 - 10.0.3.100/24

The interfaces of the switch were s1-eth1, s1-eth2 and s1-eth3 which were connected to host 1, host 2 and host 3 respectively.

3.  mytopo2.py - In this code the topology of Part B of the project was implemented. The topology consisted of five hosts and 2
switches. Host 1 and 2 were connected to switch 1 and host 3,4 and 5 were connected to switch 2. The hosts had the following IP addresses:

Host 1 - 10.0.1.2

Host 2 - 10.0.1.3

Host 3 - 10.0.2.2

Host 4 - 10.0.2.3

Host 5 - 10.0.2.4

The interfaces of the switch 1 were s1-eth1, s1-eth2 which were connected to host 1 and host 2 respectively. The interfaces of switch 2 were s2-eth1, s2-eth2 and s2-eth3 were connected to host host 3,4 and 5. s1-eth3 of switch 1 is connected to s2-eth4 of switch 2.


4. router1.py - In router1.py code file we configure the switch in the first topology. In this part I have configured a static routing table
in order to check the IP address of the hosts. In the first part of the code I check for the ARP request from the packet and reply with the MAC address of the router which is essentially a MAC ID I have created. Once this step is done then I move on to the ICMP part of the code.If the packet protocol type is ICMP then an echo reply is created which is then encapsulated into a icmp packet which is then encapsulated into an ethernet packet. After this the OpenFlow functions such of.ofp_packet_out(), of.ofp_action_output() and connection.send() messages are used. Then static routing part is done and the packets are sent to the IP address indicated. This is done by finding the IP address in the routing table and sending it to the corresponding device.  


5. router2.py - In this code most of the function is similar to that of router1.py except that there are three static routing table. This is because there are two different switches and the MAC addresses need to be different in both the cases. So there are two fake MAC addresses created for switches 1 and 2. In this case when it comes to ARP requests it checks the origination of the packet and whether it comes from subnet 1 or subnet 2, if it comes from subnet 1 then it will sent the MAC ID of the first switch otherwise it will send the MAC ID of switch 2.After this it goes to the ICMP request part, it checks whether the ICMP request comes from router 1 by checking the MAC ID and if it belongs to switch 1 then it checks the routing table whether the host is available in the first routing table. If it is not available in the first routing table then it says the ICMP destination is unavailable. The same process is repeated for the MAC ID of switch 2. After this we perform the static routing part where the MAC id of the packet is checked again then sent to the corresponding MAC IDs obtained from the routing table.


INSTRUCTIONS ON RUNNING THE CODE FILE:

1. This project requires Mininet and VirtualBox softwares in order to function in the correct manner

For learning switch part:

2. From the mininet console:
$ sudo mn -c
$ sudo mn --topo single, 3 --mac --switch ovsk --controller remote

3. On a different terminal

./pox.py log.level --DEBUG misc.of_tutorial 

$ sudo killall controller 


Part A:

1. Put router1.py in the path /home/mininet/pox/pox/misc
2. Put mytopo1.py in the path /home/mininet

$ sudo mn -c
$ sudo mn --custom mytopo1.py --topo mytopo --mac --switch ovsk --controller remote

3. For the controller part:

In /home/mininet/pox

./pox.py log.level --DEBUG misc.router1 misc.full_payload

4. To check the packet traffic on any interface

tcpdump -xx -n -i <interface_name>

Part B:

1. Put router2.py in the path /home/mininet/pox/pox/misc
2. Put mytopo2.py in the path /home/mininet

$ sudo mn -c
$ sudo mn --custom mytopo2.py --topo mytopo --mac --switch ovsk --controller remote

3. For the controller part:

In /home/mininet/pox

./pox.py log.level --DEBUG misc.router2 misc.full_payload

4. To check the packet traffic on any interface

tcpdump -xx -n -i <interface_name>


