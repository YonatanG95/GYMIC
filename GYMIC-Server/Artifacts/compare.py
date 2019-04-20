from datetime import datetime
from elastic_util import ElasticUtil
import socket
from elastic_util import ElasticUtil
from user_threads import UserThreads
from kernel_threads import KernelThreads
from user_processes import UserProcesses
from kernel_processes import KernelProcesses
from conf import LIME_PORT

def compare_proc(artifacts_list, addr):

    irelevant_processes = ["ksoftirqd", "rcu_sched", "insmod", "system-udevd", "ps", "sh", "lsched"]
    for artifact in artifacts_list:
        if artifact.artifact_type is UserProcesses:
            list1 = artifact.parsed_data
        elif artifact.artifact_type is KernelProcesses:
            list2 = artifact.parsed_data
    ##Get a list of processes that are not in both lists
    diff_list =  [i for i in list1 + list2 if i not in list1 or i not in list2]
    #Delete from the diff list procceses that we know that suppose to be there
    for proc in diff_list:
        for p in irelevant_processes:
            if proc[-1] in p:
                diff_list.remove(proc)
    #Creating a socket so the server will memdump the workstation


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, LIME_PORT))
    if len(diff_list)==0:
        s.sendall("Yes")
    else:
        s.sendall("No")
    s.close()


    #If the list is not empty, we know that there are processes that are not in both user and kernel and we want to
    #send packet to the server to take memdump.
    es_util = ElasticUtil()
    for tup in diff_list:
        if tup in list1:
             doc = {"timestamp": datetime.utcnow(),
                   "IP": addr,
                   "UserProcesses.PID": tup[0],
                   "UserProcesses.ProcessName": tup[-1],
                   "inUser:": True,
                   "inKernel:": False}

            # Connection successful

             es_util.send_to_elastic("gymic-compareprocess", "ProcessCompare", doc)
        elif tup in list2:

            doc = {"timestamp": datetime.utcnow(),
                         "IP": addr,
                         "KernelProcesses.PID": tup[0],
                         "KernelProcesses.ProcessName": tup[-1],
                         "inUser:": False,
                         "inKernel:": True}

            # Connection successful
            es_util.send_to_elastic("gymic-compareprocess", "ProcessCompare", doc)



def compare_threads(artifacts_list, addr):

    for artifact in artifacts_list:
        if artifact.artifact_type is UserThreads:
            list1 = artifact.parsed_data
        elif artifact.artifact_type is KernelThreads:
            list2 = artifact.parsed_data

    diff_list =  [i for i in list1 + list2 if i not in list1 or i not in list2]
    es_util = ElasticUtil()
    for tup in diff_list:
        if tup in list1:
            doc = {"timestamp": datetime.utcnow(),
                         "IP": addr,
                         "UserThread.PID": tup[0],
                         "UserThread.TID": tup[-1],
                         "inUser:": True,
                         "inKernel:": False}

            # Connection successful
            es_util.send_to_elastic("gymic-comparethreads", "ThreadCompare", doc)
        elif tup in list2:
            doc = {"timestamp": datetime.utcnow(),
                         "IP": addr,
                         "KernelThread.PID": tup[0],
                         "KernelThread.TID": tup[-1],
                         "inUser:": False,
                         "inKernel:": True}

            # Connection successful
            es_util.send_to_elastic("gymic-comparethreads", "ThreadCompare", doc)