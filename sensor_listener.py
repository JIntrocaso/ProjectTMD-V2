import logging
import sys, os
import resource

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from pydispatch import dispatcher
import time

device="/dev/ttyACM0"
log="Debug"

options = ZWaveOption(device, \
    config_path="venv3/lib/python3.6/site-packages/python_openzwave/ozw_config/", \
    user_path=".", \
    cmd_line="" \
    )
options.set_log_file("SensorListener_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
options.set_logging(False)
options.lock()

network = ZWaveNetwork(options, log=None)

def louie_network_started(network):
    print("Hello from the network: I'm started : homeid %0.8x - %d nodes were found." %(network.home_id, network.nodes_count))

def louie_network_ready(network):
    print("Hello from network : I'm ready : %d nodes were found." % network.nodes_count)
    print("Hello from network : my controller is : %s" % network.controller)

def louie_network_failed(network):
    print("Hello from network : can't load. :(")

def louie_node_update(network, node):
    print('Louie signal : Node update : {}.'.format(node))

def louie_value_update(network, node, value):
    valueData = value.data
    # nodeInfo = value.to_dict()
    # for val in nodeInfo:
    #     print("{}: {}".format(val, nodeInfo[val]))
    if (valueData == 22):
        print("Node {}: Opened".format(value.node.node_id))
    if (valueData == 23):
        print("Node {}: Closed".format(value.node.node_id))

def initialize_node_listeners(network):
    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)
    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_NOTIFICATION)
    dispatcher.disconnect(initialize_node_listeners, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)

dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
dispatcher.connect(initialize_node_listeners, ZWaveNetwork.SIGNAL_NODE_QUERIES_COMPLETE)

network.start()
count = 0
while True:
    sys.stdout.write(".")
    sys.stdout.flush()
    count += 1
    time.sleep(1.0)


