
from pox.core import core
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pk
import pox.lib.addresses as adr

log = core.getLogger()

class Router (object):


  def FlowMode(self, packeti, out_port):
       mg = of.ofp_flow_mod()
       mg.match.in_port = packeti.in_port
       mg.idle_timeout = 120
       mg.buffer_id = packeti.buffer_id
       mg.actions.append(of.ofp_action_output(port = out_port))
       log.debug("Entered flow mode")

  def find_key(self,ip_p):
     i=0
     for key in self.rtable.keys():
        if ip_p.dstip.inNetwork(key):
          i = key
          return i

  def open_flow_func(self,packeti,port1,eth):
     mg=of.ofp_packet_out()
     mg.data = eth.pack()
     if packeti !=0:
     	mg.actions.append(of.ofp_action_output(port = packeti.in_port))
     else:
	mg.actions.append(of.ofp_action_output(port = port1))
     self.connection.send(mg)
	

  def __init__ (self, connection):

    self.connection = connection

    connection.addListeners(self)

    self.rtable = {'10.0.1.0/24': ['s1-eth1', '10.0.1.100','10.0.1.1','00:00:00:00:00:01',1], '10.0.2.0/24': ['s1-eth2','10.0.2.100','10.0.2.1','00:00:00:00:00:02',2], '10.0.3.0/24': ['s1-eth3','10.0.3.100','10.0.3.1','00:00:00:00:00:03',3]}

  def create_router(self, packet, packeti):

        if packet.type == pk.ethernet.ARP_TYPE:
            if packet.payload.opcode == pk.arp.REQUEST:
                log.debug('ARP REQUEST RECEIVED')  
                reply = pk.arp()
                reply.opcode = pk.arp.REPLY
                reply.hwdst = packet.payload.hwsrc
                reply.hwsrc = adr.EthAddr('AC:AC:AC:AC:AC:BD')
                reply.protosrc = packet.payload.protodst
                reply.protodst = packet.payload.protosrc
                e = pk.ethernet(type=pk.ethernet.ARP_TYPE,src=packet.dst,dst=packet.src)
                e.set_payload(reply)
		self.open_flow_func(packeti,0,e)      
                log.debug('ARP REPLY SENT')
            else:
                log.debug('ARP REPLY')
     

        elif packet.type == pk.ethernet.IP_TYPE:
           ip_u = packet.payload
           if ip_u.protocol == pk.ipv4.ICMP_PROTOCOL:
                icmp_p = ip_u.payload
                #Find whether the host is available in the routing table
                if icmp_p.type == pk.TYPE_ECHO_REQUEST:
                    log.debug('ICMP REQUEST RECEIVED')
                    n = self.find_key(ip_u)
		    log.debug(n)                  
                    if n!=None:
                        log.debug('ICMP Reply Sent') 
                        icmp_r = pk.icmp()
                        icmp_r.type = pk.TYPE_ECHO_REPLY
                        #Insert the echo payload into the reply packet
                        icmp_r.set_payload(packet.find("icmp").payload)
                        #Create an ipv4 packet and insert the ICMP 
			ip_encap = pk.ipv4(srcip = ip_u.dstip,dstip = ip_u.srcip,protocol = pk.ipv4.ICMP_PROTOCOL)
                        ip_encap.set_payload(icmp_r)
                        #Create an Ethernet packet and insert the IPV4 in it
                        eth_encap = pk.ethernet(type = pk.ethernet.IP_TYPE,src =packet.dst,dst = packet.src)
                        eth_encap.set_payload(ip_encap)
                        self.open_flow_func(packeti,0,eth_encap)
                        #Get the payload from echo request
		    else:
                        u = pk.unreach()
                        u.payload = ip_u
			log.debug("Destination Unreachable")
                        #Create an echo reply packet 
                        icmp_r = pk.icmp()
                        icmp_r.type = pk.TYPE_DEST_UNREACH
			icmp_r.code = pk.CODE_UNREACH_HOST
                        #Insert the echo payload into the reply packet
                        icmp_r.payload = u
                        #Create an ipv4 packet and insert the ICMP
                        ip_encap = pk.ipv4()
			ip_encap = pk.ipv4(srcip = ip_u.dstip,dstip=ip_u.srcip,protocol = pk.ipv4.ICMP_PROTOCOL)
                        ip_encap.set_payload(icmp_r)                  
                        #Create an Ethernet packet and insert the IPV4 in it
                        eth_encap = pk.ethernet(type = pk.ethernet.IP_TYPE, src = packet.dst, dst = packet.src)
                        eth_encap.set_payload(ip_encap)
			self.open_flow_func(packeti,0,eth_encap)
           else:
                 j=0
                 j = self.find_key(ip_u)                    
                 if j!=0:
		     dsthw = self.rtable[j][3]
                     p = self.rtable[j][4]
                     dsthw1 = adr.EthAddr(dsthw)
                     
                     packet.src = packet.dst
                     packet.dst = dsthw1
		     self.open_flow_func(0,p,packet)                                              
           self.FlowMode( packeti, packeti.in_port)                          

  def _handle_PacketIn (self, event):
        packet = event.parsed
        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return
        packeti = event.ofp
        self.create_router(packet,packeti)

def launch ():
        def start_switch (event):
         log.debug("Controlling %s" % (event.connection,))
         Router(event.connection)
        core.openflow.addListenerByName("ConnectionUp", start_switch)



