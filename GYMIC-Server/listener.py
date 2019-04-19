import zmq
import threading
import socket
from conf import ZMQ_SERVER_PORT, ZMQ_WORKER_PORT, ZMQ_SERVER_IP, TCP_SERVER_IP, TCP_SERVER_PORT
import random
from Artifacts.artifact import Artifact


def zmqserver():

    context = zmq.Context()
    server_socket = context.socket(zmq.PULL)
    try:
        server_socket.bind("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_SERVER_PORT))
    except Exception as e:
        print e.message
    try:
        while True:
            result = server_socket.recv_json()
            if result.has_key('worker_id'):
                print "Worker {} finished printing".format(result["worker_id"])
    except Exception as e:
        print e.message


def zmqworker():

    worker_id = random.randrange(1, 10005)
    print "Worker {0} has started.".format(worker_id)
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    try:
        pull_socket.connect("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_WORKER_PORT))
    except Exception as e:
        print e.message

    push_socket = context.socket(zmq.PUSH)
    try:
        push_socket.connect("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_SERVER_PORT))
    except Exception as e:
        print e.message

    try:
        while True:
            # Wait for next request from client
            msg = pull_socket.recv()
            print "Worker {0} Received request: {1}".format(worker_id, msg)

            if msg is not None:
                # Code for actual work
                result = {"worker_id" : worker_id, 'data' : msg}
                artifact = Artifact(msg)
                artifact.parse_to_json()
                artifact.send_to_elastic()
                #TODO: Add send_to_elastic and parse_to_json here, and handle not all data recieved in one socket. PARSED DATA IS IN DESKTOP gymicOUTPUT.TXT

                push_socket.send_json(result)
    except Exception as e:
        print e.message

def zmqsender(msg):

    try:
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUSH)
        zmq_socket.bind("tcp://{}:{}".format(ZMQ_SERVER_IP, ZMQ_WORKER_PORT))
        zmq_socket.send(msg)
        zmq_socket.close()
    except Exception as e:
        print e.message

def tcpserver():

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((TCP_SERVER_IP, TCP_SERVER_PORT))
        sock.listen(1)
    except Exception as e:
        print e.message

    while True:
        conn, addr = sock.accept()
        try:
            while True:
                data = conn.recv(4096*5)
                if data:
                    zmqsender(data)
                else:
                    break
        except Exception as e:
            print e.message

        finally:
            conn.close()

def main():
    thread_zmqserver = threading.Thread(target=zmqserver)
    thread_zmqserver.daemon = True
    thread_zmqserver.start()
    workers = []
    for i in xrange(1):
        worker = threading.Thread(target=zmqworker)
        worker.daemon = True
        workers.append(worker)
        worker.start()

    tcpserver()


if __name__ == '__main__':
    main()




