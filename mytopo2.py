
from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def __init__( self):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        host1 = self.addHost( 'h1', ip="10.0.1.2", defaultRoute = "via 10.0.1.1/24" )
        host2 = self.addHost( 'h2', ip="10.0.1.3", defaultRoute = "via 10.0.1.1/24" )
        host3 = self.addHost( 'h3', ip="10.0.2.2", defaultRoute = "via 10.0.2.1/24" )

	host4 = self.addHost( 'h4', ip="10.0.2.3", defaultRoute = "via 10.0.2.1/24" )
        host5 = self.addHost( 'h5', ip="10.0.2.4", defaultRoute = "via 10.0.2.1/24" )

        switch1 = self.addSwitch( 's1')
	switch2 = self.addSwitch( 's2')


        # Add links
        self.addLink( host1, switch1 )
        self.addLink( host2, switch1 )
        self.addLink( host3, switch2 )
	self.addLink( host4, switch2 )
	self.addLink( host5, switch2 )
	self.addLink( switch1, switch2 )
	



topos = { 'mytopo': ( lambda: MyTopo() ) }

