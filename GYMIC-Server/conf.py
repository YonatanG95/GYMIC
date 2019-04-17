from Artifacts.UserThreads import UserThreads
# All Configurations

# ZMQ Configurations
ZMQ_SERVER_IP = "127.0.0.1"
ZMQ_SERVER_PORT = 5558
ZMQ_WORKER_PORT = 5557

# TCP Server Configurations
TCP_SERVER_IP = "0.0.0.0"
#TCP_SERVER_PORT = 1234
TCP_SERVER_PORT = 1234

# ELK Configurations
ELK_SERVER_IP = "192.168.1.54"
ELK_SERVER_PORT = 9200

# Artifact Configurations
ARTIFACT_DICT = {}
ARTIFACT_DICT["userThreads"] = UserThreads