import zmq
import threading
import socket
import random
import json

from conf import ZMQ_SERVER_PORT, ZMQ_WORKER_PORT, ZMQ_SERVER_IP, TCP_SERVER_IP, TCP_SERVER_PORT, NUM_OF_WORKERS
from Artifacts.artifact import Artifact
from Artifacts.compare import compare_proc,compare_threads
from elastic_util import ElasticUtil
from utils import recv_dump

# Output dict, Key-Value: IP-Artifacts list
output_dict = {}


def zmqserver():

    context = zmq.Context()
    server_socket = context.socket(zmq.PULL)
    try:
        server_socket.bind("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_SERVER_PORT))
    except Exception as e:
        es = ElasticUtil()
        es.log_error("ZMQServer BindError: " + e.message)
    try:
        while True:
            result = server_socket.recv_json()
            if result.has_key('worker_id'):
                print "Worker {} finished printing".format(result["worker_id"])
    except Exception as e:
        es = ElasticUtil()
        es.log_error("ZMQServer ReceiveError: " + e.message)


def zmqworker():

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

                if msg.startswith("gymic_finish_thread"):

                    compare_threads(output_dict[addr], addr)
                    pass
                elif msg.startswith("gymic_finish_proc"):

                    compare_proc(output_dict[addr], addr)
                    pass

                elif msg.startswith("gymic_finish_mod"):

                    #TODO: Modules Compare function here for Amir
                    pass

                artifact = Artifact(msg, addr)
                artifact.parse_to_json()
                artifact.send_to_elastic()

                # Add to output dictionary
                if artifact.artifact_type != None:
                    if output_dict.has_key(addr):
                        output_dict[addr].append(artifact)
                    else:
                        output_dict[addr] = [artifact]

                push_socket.send_json(result)
    except Exception as e:
        es = ElasticUtil()
        es.log_error("ZMQWorker ReceiveError: " + e.message)

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

def tcpserver():

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((TCP_SERVER_IP, TCP_SERVER_PORT))
        sock.listen(1)
    except Exception as e:
        es = ElasticUtil()
        es.log_error("TCPServer BindError: " + e.message)

    while True:
        conn, addr = sock.accept()
        try:
            while True:
                data = conn.recv(4096*5)
                if data:
                    msg = {"data": data, "addr" : addr[0]}
                    zmqsender(json.dumps(msg))
                else:
                    break
        except Exception as e:
            es = ElasticUtil()
            es.log_error("TCPServer ReceiveError: " + e.message)

        finally:
            conn.close()

def main():

    try:
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




