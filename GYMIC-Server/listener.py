import zmq
import threading
import socket
import random
import json

from conf import ZMQ_SERVER_PORT, ZMQ_WORKER_PORT, ZMQ_SERVER_IP, TCP_SERVER_IP, TCP_SERVER_PORT, NUM_OF_WORKERS
from Artifacts.artifact import Artifact
from Artifacts.compare import compare_proc,compare_threads,compare_modules, searchForMiner
from elastic_util import ElasticUtil
from utils import recv_dump

# Output dict, Key-Value: IP-Artifacts list
output_dict = {}

# initialize zmqserver
def zmqserver():

    context = zmq.Context()
    server_socket = context.socket(zmq.PULL)
    try:
        server_socket.bind("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_SERVER_PORT))
    except Exception as e:
        es = ElasticUtil()
        es.log_error("ZMQServer BindError: " + e.message)

    while True:
        try:
            while True:
                result = server_socket.recv_json()
                if result.has_key('worker_id'):
                    print "Worker {} finished printing".format(result["worker_id"])
        except Exception as e:
            es = ElasticUtil()
            es.log_error("ZMQServer ReceiveError: " + e.message)


def zmqworker():
    # Initialize worker
    worker_id = random.randrange(1, 10005)
    print "Worker {0} has started.".format(worker_id)
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    try:
        pull_socket.connect("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_WORKER_PORT))
    except Exception as e:
        es = ElasticUtil()
        es.log_error("ZMQWorker PullConnectError: " + e.message)

    push_socket = context.socket(zmq.PUSH)
    try:
        push_socket.connect("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_SERVER_PORT))
    except Exception as e:
        es = ElasticUtil()
        es.log_error("ZMQWorker PushConnectError: " + e.message)

    while True:
        try:
            while True:
                # Wait for next request from client
                msg_json = pull_socket.recv()
                msg_dic = json.loads(msg_json)
                msg = msg_dic.get("data")
                addr = msg_dic.get("addr")
                print "Worker {0} Received request: {1}".format(worker_id, msg)
                if msg is not None:
                    # Code for actual work
                    result = {"worker_id" : worker_id, 'data' : msg}

                    # Check the data type and act accordingly (parse and analyze data and send it to elastic)
                    if msg.startswith("gymic_finish_thread"):
                        compare_threads(output_dict[addr], addr)

                    elif msg.startswith("gymic_finish_proc"):
                        compare_proc(output_dict[addr], addr)
                        try:
                            net = output_dict[addr]["userNetwork"]
                            searchForMiner(output_dict[addr], addr)
                        except KeyError:
                            pass

                    elif msg.startswith("gymic_finish_mod"):
                        compare_modules(output_dict[addr], addr)

                    elif msg.startswith("gymic_finish_net"):
                        try:
                            proc = output_dict[addr]["userProcess"]
                            searchForMiner(output_dict[addr], addr)
                        except KeyError:
                            pass


                    if "finish" not in msg:
                        artifact = Artifact(msg, addr)
                        artifact.parse_to_json()
                        artifact.send_to_elastic()

                        # Add to output dictionary
                        if artifact.artifact_type is not None:
                            if output_dict.has_key(addr):
                                try:
                                    output_dict[addr][artifact.artifact_header] = artifact
                                except KeyError:
                                    pass
                            else:
                                output_dict[addr] = {}
                                output_dict[addr][artifact.artifact_header] = artifact

                        push_socket.send_json(result)

        except Exception as e:
            es = ElasticUtil()
            es.log_error("ZMQWorker ReceiveError: " + e.message)

# Get the data from tcp server and send in to zmqserver
def zmqsender(msg):

    try:
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_WORKER_PORT))
        zmq_socket.send(msg)
        zmq_socket.close()
    except Exception as e:
        es = ElasticUtil()
        es.log_error("ZMQSender SendError: " + e.message)

# Initialize the tcp server to receive the data from the clients and pass is to zmqserver
def tcpserver():

    try:
        # Initialize server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((TCP_SERVER_IP, TCP_SERVER_PORT))
        sock.listen(10)
    except Exception as e:
        es = ElasticUtil()
        es.log_error("TCPServer BindError: " + e.message)

    completed = ""
    # Infinite loop to receive data from clients
    while True:
        conn, addr = sock.accept()
        try:
            while True:
                data = conn.recv(65536)
                completed = completed + data

                if "End" in completed:
                    msg = {"data": completed[:completed.find("End")], "addr": addr[0]}
                    # Send the data to zmqserver
                    zmqsender(json.dumps(msg))
                    completed = completed[completed.find("End") + 7:]

                else:
                   break

        except Exception as e:
            es = ElasticUtil()
            es.log_error("TCPServer ReceiveError: " + e.message)



def main():

    try:
        # initializing zmqserver and workers and their function
        thread_zmqserver = threading.Thread(target=zmqserver)
        thread_zmqserver.daemon = True
        thread_zmqserver.start()
        workers = []
        for i in xrange(NUM_OF_WORKERS):
            worker = threading.Thread(target=zmqworker)
            worker.daemon = True
            workers.append(worker)
            worker.start()

    except Exception as e:
        es = ElasticUtil()
        es.log_error("Threads StartError: " + e.message)

    tcpserver()


if __name__ == '__main__':
    main()




