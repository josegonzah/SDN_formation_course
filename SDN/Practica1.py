from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSSwitch
from mininet.nodelib import LinuxBridge
import sys

class CustomTopo(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)

        hosts = []
        switches = []
        for i in range(0, int(sys.argv[1])):
        
            h = self.addHost('h'+ str(i))
            hosts.append(h)
            s = self.addSwitch('s' + str(i), cls=OVSSwitch, stp=1)
            switches.append(s)

        for j in range(0, int(sys.argv[1])):
            for i in range(j, int(sys.argv[1])):
                self.addLink(h[j], s[i])
                
def runNet():
    topo = CustomTopo()
    net = Mininet(topo)
    net.start()
    net.pingAll()
    net.pingAll()
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    runNet()
