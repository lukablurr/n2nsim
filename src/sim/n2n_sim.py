'''
N2N Simulator
'''
#TODO from n2npy import *
import os
import time
import socket
import struct
import pcap
import nfqueue
import signal
from subprocess import call
from socket import AF_INET, AF_INET6, inet_ntoa
from dpkt import ip

from sim.filter import Filter
from server.serversim import ServerSim
from client.n2n_community import N2NCommunity
from client.clientsim import ClientSim



def ip2int(addr):                                                               
    return struct.unpack("!I", socket.inet_aton(addr))[0]                       


def int2ip(addr):                                                               
    return socket.inet_ntoa(struct.pack("!I", addr)) 


class N2NSimulator(object):
    
    DEFAULT_IFACE =  "eth0:0"
    DEFAULT_COMM_NAME = "community"
    
    QUEUE_NUM = 0
    
    MAX_CLIENTS_PER_COMMUNITY = 1
    
    SERVER_PORT = 44000
    SERVER_MPORT = 45000
    
    SN_IP_RANGE_START = ip2int("33.0.0.1")
    
    EDGE_PORT = 46000
    
    EDGE_IP_RANGE_START = ip2int("33.0.0.101")
    
    
    
    def __init__(self):
        self.servers = []
        self.communities = []
        self.iface = N2NSimulator.DEFAULT_IFACE
        self.filter = None
        
    def __del__(self):
        print("destroy simulator")
        if self.filter:
            self.filter.stop()
            self.filter.join()
            self.filter = None
        
    def setSupernodePath(self, path):
        from server.supernode import Supernode#TODO
        Supernode.PATH = path
        
    def setEdgePath(self, path):
        from client.edge import Edge#TODO
        Edge.PATH = path
        
    def configQueue(self, bool_add):
        iptables_args = [ "iptables", ("-A" if bool_add else "-D"), 
                          "INPUT", "-m", "iprange", 
                          "--src-range", "33.0.0.1-33.0.0.255", 
                          "--dst-range", "33.0.0.1-33.0.0.255", 
                          "-j", "NFQUEUE", "--queue-num", ("%d" % (N2NSimulator.QUEUE_NUM)) 
                        ]
        #TODO enable iptables_args = ["iptables", "-A", "INPUT", "-p", "udp", "-m", "udp", "--sport", "44000:44999", "--dport", "44000:44999", "-j", "NFQUEUE", "--queue-num", "0"]
        call(iptables_args)

    def initEnvironment(self):
        '''
        ifconfig eth0:0 33.0.0.1 netmask 255.255.255.0 up
        iptables -A INPUT -m iprange --src-range 33.0.0.1-33.0.0.255 --dst-range 33.0.0.1-33.0.0.255  -j NFQUEUE --queue-num 0
        '''
        ifconfig_args = [ "ifconfig", self.iface, "33.0.0.1", 
                          "netmask", "255.255.255.0", 
                          "up"
                        ]
        call(ifconfig_args)
        self.configQueue(True)
        
    def startClient(self, client):
        ip_args = [ "ip", "addr", "add", client.ip, "broadcast", "33.0.0.255", "dev", self.iface ]
        call(ip_args)

    def stopClient(self, client):#TODO remove
        ip_args = ["ip", "addr", "del", client.ip, "dev", self.iface]
        call(ip_args)
        
    # Servers ------------------------------------------------------------------
        
    def createServers(self, servers_num):
        prev_addr = None
        for i in range(servers_num):
            server = ServerSim()
            sn = server.supernode
            # Local address
            addr = int2ip( N2NSimulator.SN_IP_RANGE_START + i )
            port = "%s:%d" % (addr, N2NSimulator.SERVER_PORT + i)
            sn.params.port.setValue(port)
            # Local management address
            mport = "127.0.0.1:%d" % (N2NSimulator.SERVER_MPORT + i)
            sn.params.mgmt_port.setValue(mport)
            # Peer supernode address
            if prev_addr:
                sn.params.supernode.setValue(prev_addr)
            
            self.servers.append(server)
            prev_addr = port
            
    def startServers(self):
        for server in self.servers:
            server.supernode.run()
            time.sleep(3)
            
    def stopServers(self):
        for server in self.servers:
            server.supernode.stop()
    
    
    # Clients ------------------------------------------------------------------
    
    def createCommunities(self, communities_num):
        for i in range(communities_num):
            name = "%s%03d" % (N2NSimulator.DEFAULT_COMM_NAME, i)
            print ("Creating %s community" % (name))
            
            community = N2NCommunity(name, None)
            
            for j in range(N2NSimulator.MAX_CLIENTS_PER_COMMUNITY):
                #-d n2n0 -u 99 -g 99 -m 3C:A0:12:34:56:78 -a dhcp:1.2.3.4 -l 192.168.1.102:7777
                #TODO macs and ips
                addr = int2ip( N2NSimulator.EDGE_IP_RANGE_START + i * j )
                client = ClientSim(addr)
                edge = client.edge
                port = "%s:%d" % (addr, N2NSimulator.EDGE_PORT + i * j)
                edge.params.port.setValue(port)
                edge.params.super_addr.setValue("%s:%s" % (int2ip(N2NSimulator.SN_IP_RANGE_START), N2NSimulator.SERVER_PORT))#TODO
                edge.params.device_name.setValue("n2n%02d" % (i * j))
                edge.params.device_mac.setValue("3C:A0:12:34:56:78")#TODO
                edge.params.device_addr.setValue("1.2.3.4")#TODO
                
                community.addMember(client)
                
            self.communities.append(community)
    
    def startCommunities(self):
        for c in self.communities:
            for m in c.members:
                self.startClient(m)
                m.edge.run()
                time.sleep(3)
    
    def stopCommunities(self):
        for c in self.communities:
            for m in c.members:
                m.edge.stop()
                self.stopClient(m)
                
    # Simulator states ---------------------------------------------------------
    
    def init(self, servers_num, communities_num):
        self.createServers(servers_num)
        self.createCommunities(communities_num)
                
    def start(self):
        self.initEnvironment()
        self.filter = Filter(N2NSimulator.QUEUE_NUM, self.handleUdp)
        self.filter.start()
        self.startServers()
        self.startCommunities()
        
    def stop(self):
        print("stopping simulator")
        self.stopCommunities()
        self.stopServers()
        self.filter.stop()
        self.filter.join()
        self.filter = None
        self.configQueue(False)
        
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
