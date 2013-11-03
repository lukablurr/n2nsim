import sys
import signal
import debug
from sim.n2n_sim import N2NSimulator

n2nsim = None


def main(config_file):
    debug.traceMe()
    N2NSimulator.configure(config_file)
    # Set handler for signals
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)
    # Create simulator
    global n2nsim
    n2nsim = N2NSimulator()
    n2nsim.init()
    # Start the simulator
    n2nsim.start()
    #TODO
    #n2nsim.stop()


def terminate(sig, frame):
    global n2nsim
    print("terminating....")
    n2nsim.stop()


if __name__=='__main__':
    main(sys.argv[1])

