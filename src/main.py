import sys
import signal
import debug
from sim.n2n_sim import N2NSimulator


SERVERS_NUM = 1
COMMUNITIES_NUM = 1

n2nsim = None


def main(supernode_path, edge_path):
    debug.traceMe()
    global n2nsim
    n2nsim = N2NSimulator()
    n2nsim.setSupernodePath(supernode_path)
    n2nsim.setEdgePath(edge_path)
    n2nsim.init(SERVERS_NUM, COMMUNITIES_NUM)
    # Set handler for signals
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    # Start the simulator
    n2nsim.start()
    #TODO
    n2nsim.stop()


def terminate(sig, frame):
    global n2nsim
    n2nsim.stop()


if __name__=='__main__':
    main(sys.argv[1], sys.argv[2])

