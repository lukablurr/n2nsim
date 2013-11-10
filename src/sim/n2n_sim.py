'''
N2N Simulator
'''
#TODO from n2npy import *

import time
import nfqueue
from socket import inet_ntoa
from dpkt import ip

from sim.simcfg import SimulatorConfig
from sim.filter import Filter
from server.serversim import ServerSim
from client.community import N2NCommunity
from client.clientsim import ClientSim
from utils.net import int2ip
from utils.iprange import IpRange
from utils.tools import run_cmd


class N2NSimulator(object):
    
    CONFIG = SimulatorConfig()
    INTERVAL = 3
    
    def __init__(self):
        self.servers = []
        self.communities = []
        self.filter = None
        self.running = False
        
    def __del__(self):
        print("destroy simulator")
        if self.filter:
            self.filter.stop()
            self.filter.join()
            self.filter = None
        
    def configQueue(self, bool_add):
        op = ("-A" if bool_add else "-D") # add/delete
        queue = ("%d" % (N2NSimulator.CONFIG.queue))
        # Merge ranges
        my_range = IpRange( min(ServerSim.CONFIG.ip_range.start,
                                ClientSim.CONFIG.ip_range.start),
                            max(ServerSim.CONFIG.ip_range.end,
                                ClientSim.CONFIG.ip_range.end) )
        my_range_str = my_range.toString()
        # iptables: move to netfilter queue
        iptables_args = [ "iptables", op, 
                          "INPUT", "-m", "iprange", 
                          "--src-range", my_range_str, 
                          "--dst-range", my_range_str, 
                          "-j", "NFQUEUE", "--queue-num", queue 
                        ]
        run_cmd(iptables_args)

    def initEnvironment(self):
        self.configQueue(True)
        ServerSim.CONFIG.initEnvironment()
        ClientSim.CONFIG.initEnvironment()
        
    # Servers ------------------------------------------------------------------
        
    def createServers(self):
        prev_addr = None
        for i in range(ServerSim.CONFIG.max):
            # Local address
            ip = ServerSim.CONFIG.ip_range.start + i
            port = ServerSim.CONFIG.port + i
            # Local management port
            mport = ServerSim.CONFIG.mport + i
            # Server instance
            server = ServerSim(ip, port, mport, prev_addr)
            
            self.servers.append(server)
            prev_addr = (ip, port)
            
    def startServers(self):
        for server in self.servers:
            server.start()
            time.sleep(3)
            
    def stopServers(self):
        for server in self.servers:
            server.stop()
    
    
    # Clients ------------------------------------------------------------------
    
    def createCommunities(self):
        super_addr = "%s:%s" % ( int2ip(ServerSim.CONFIG.ip_range.start), 
                                 ServerSim.CONFIG.port )
        
        for i in range(N2NCommunity.CONFIG.max):
            name = "%s%03d" % (N2NCommunity.CONFIG.name_prefix, i)
            print ("Creating %s community" % (name))
            
            community = N2NCommunity(name, None)
            
            for j in range(N2NCommunity.CONFIG.max_clients):
                #-d n2n0 -u 99 -g 99 -m 3C:A0:12:34:56:78 -a dhcp:1.2.3.4 -l 192.168.1.102:7777
                #TODO macs and ips
                # Local address
                ip = ClientSim.CONFIG.ip_range.start + i * j
                port = ClientSim.CONFIG.port + i * j
                
                client = ClientSim(ip, port, 0)
                
                edge = client.edge
                #edge.params.port.setValue(port)
                edge.params.super_addr.setValue(super_addr)#TODO
                edge.params.device_name.setValue("n2n%02d" % (i * j))
                edge.params.device_mac.setValue("3C:A0:12:34:56:78")#TODO
                edge.params.device_addr.setValue("1.2.3.4")#TODO
                
                community.addMember(client)
                
            self.communities.append(community)
    
    def startCommunities(self):
        for c in self.communities:
            for m in c.members:
                m.start()
                time.sleep(3)
    
    def stopCommunities(self):
        for c in self.communities:
            for m in c.members:
                m.stop()
    
    # Simulator states ---------------------------------------------------------
    
    def init(self):
        self.createServers()
        self.createCommunities()
    
    def start(self):
        try:
            self.initEnvironment()
            self.filter = Filter(N2NSimulator.CONFIG.queue, self.handleUdp)
            self.filter.start()
            self.startServers()
            self.startCommunities()
        except Exception as e:
            print("Error: %s" % str(e))
            self.stop()
            return
        self.running = True
        self.run()
    
    def run(self):
        while self.running:
            self.filter.join(timeout=3)
        self.stop()
        
    def stop(self):
        if not self.running:
            return
        print("stopping simulator")
        self.stopCommunities()
        self.stopServers()
        if self.filter and self.filter.is_alive():
            self.filter.stop()
            self.filter.join()
        self.filter = None
        ServerSim.CONFIG.deinitEnvironment()
        ClientSim.CONFIG.deinitEnvironment()
        self.configQueue(False)
        self.running = False
        
    # Running ------------------------------------------------------------------
    
    def handleUdp(self, payload):
        print ("python callback called !")
    
        data = payload.get_data()
        pkt = ip.IP(data)
        if pkt.p == ip.IP_PROTO_TCP:
            print ("  len %d proto %s src: %s:%s    dst %s:%s " % (payload.get_length(),pkt.p,inet_ntoa(pkt.src),pkt.tcp.sport,inet_ntoa(pkt.dst),pkt.tcp.dport))
        else:
            print ("  len %d proto %s src: %s    dst %s " % (payload.get_length(),pkt.p,inet_ntoa(pkt.src),inet_ntoa(pkt.dst)))
    
        payload.set_verdict(nfqueue.NF_ACCEPT)
        return 1
    
    # Statics ------------------------------------------------------------------
    
    @staticmethod
    def configure(config_file):
        N2NSimulator.CONFIG.read_from_file(config_file)
        ServerSim.CONFIG.read_from_file(config_file)
        N2NCommunity.CONFIG.read_from_file(config_file)
        ClientSim.CONFIG.read_from_file(config_file)
    
    
