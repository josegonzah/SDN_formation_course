import csv
import os
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple


#Adicione las clases y metodos que considere



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]
dictionary_mac = {}
with open(policyFile, 'r') as file:
    reader = csv.reader(file)
    counter_row = 0
    for row in reader:
        if counter_row == 0:
            counter_row += 1
        else:
            key = int(row[0])
            dictionary_mac[key] = row[1:]
            counter_row += 1
#Cree variables globales aca


class Firewall (EventMixin):

    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Activando el firewall")

    def _handle_ConnectionUp(self, event):
        #Adicione su codigo aca
        for i in dictionary_mac:
            block = of.ofp_match()
            block.dl_src = EthAddr(dictionary_mac.get(i)[0])
            block.dl_dst = EthAddr(dictionary_mac.get(i)[1])
            flow_mod = of.ofp_flow_mod()
            flow_mod.match = block
            event.connection.send(flow_mod)
            
        log.debug("Reglas instaladas en %s", dpidToStr(event.dpid))


def launch():
    core.registerNew(Firewall)
