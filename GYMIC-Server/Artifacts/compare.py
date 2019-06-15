from datetime import datetime
from time import sleep
import socket

from elastic_util import ElasticUtil
from user_threads import UserThreads
from kernel_threads import KernelThreads
from user_processes import UserProcesses
from kernel_processes import KernelProcesses
from conf import LIME_PORT
from user_modules import  UserModules
from kernel_modules import KernelModules
from utils import recv_dump
from ml import minerMLMode_inspect, minerMLMode_createModel

#is_dumped = False
mlModel = None
lableEncoderProc = None
lableEncoderUser = None


def compare_proc(artifacts_list, addr):

    print "Compare processes"
    try:
        list2 = list1 = []
        diff_list = []
        irelevant_processes = ["ksoftirqd", "rcu_sched", "insmod", "system-udevd", "ps", "sh", "lsched", "rcuos", "rcuob", "user"]

        #Signal to Workstation to not take a dump
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((addr, LIME_PORT))
        # s.send("No")
        # s.close()
        #return

        list1 = artifacts_list["userProcess"].parsed_data
        list2 = artifacts_list["kernelProcesses"].parsed_data

        if not (len(list1) == 0 or len(list2) == 0):
            tempList = []
            #print "l1: " + str(len(list1))
            #print "l2: " + str(len(list2))
            for proc in list1:
                tempList.append((proc[0], proc[2]))
            # Get a list of processes that are not in both lists
            diff_list = [i for i in tempList + list2 if i not in tempList or i not in list2]

        print diff_list

        print "diff prev: " + str(len(diff_list))

        # Delete from the diff list procceses that we know that suppose to be there
        #for proc in diff_list:
        #    if proc[-1] in irelevant_processes or proc[-1] == '':
        #        diff_list.remove(proc)
        for proc in list(diff_list):
            if proc[1] != '':
                for p in irelevant_processes:
                    if p in proc[1]:
                        diff_list.remove(proc)
                        break
            else:
                diff_list.remove(proc)

        print diff_list
        print "diff new: " + str(len(diff_list))
        #if not is_dumped:

            # Creating a socket so the server will memdump the workstation
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((addr, LIME_PORT))
            if len(diff_list) == 0:
                s.send("No")
                s.close()
            else:
                s.send("Yes")
                s.close()
                #is_dumped = True
                recv_dump(addr)
        except:
            pass

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
        print "Sent diffs"
    except Exception as e:
        es = ElasticUtil()
        es.log_error("CompareProc Error: " + e.message)
        print e.message

        # If the list is not empty, we know that there are processes that are not in both user and kernel and we want to
        # send packet to the server to take memdump.




def compare_threads(artifacts_list, addr):
    print "Compare threads"
    try:

        # for artifact in artifacts_list:
        #     if artifact.artifact_type is UserThreads:
        #         list1 = artifact.parsed_data
        #     elif artifact.artifact_type is KernelThreads:
        #         list2 = artifact.parsed_data

        list1 = artifacts_list["userThreads"].parsed_data
        list2 = artifacts_list["kernelThreads"].parsed_data

        diff_list = [i for i in list1 + list2 if i not in list1 or i not in list2]
        es_util = ElasticUtil()
        if len(diff_list) != 0:
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

    except Exception as e:

        es = ElasticUtil()
        es.log_error("CompareThread Error: " + e.message)


def compare_modules(artifacts_list, addr):

    print "Compare modules"
    try:

        list3 = list2 = list1 = []
        #global is_dumped
        # timeout = 0
        # while (len(list1) == 0 or len(list2) == 0) and timeout != 10:
        #     for artifact in artifacts_list:
        #         if artifact.artifact_type is UserModules and len(list1) == 0:
        #             list1 = artifact.parsed_data
        #         elif artifact.artifact_type is KernelModules and len(list2) == 0:
        #             list2 = artifact.parsed_data
        #     sleep(1)
        #     timeout += 1
        #
        # if timeout == 10:
        #     es = ElasticUtil()
        #     if len(list1) == 0:
        #         es.log_error("CompareModule TimeOutError: UserModules not received")
        #     elif len(list2) == 0:
        #         es.log_error("CompareModule TimeOutError: KernelModules not received")
        #
        # Signal to Workstation to not take a dump
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((addr, LIME_PORT))
        # s.send("No")
        # s.close()
        # return

        list1 = artifacts_list["userModule"].parsed_data
        list2 = artifacts_list["kernelModule"].parsed_data
        list3 = artifacts_list["sysModule"].parsed_data

        # Get a list of modules that are not in both lists
        diff_list1 = [i for i in list1 + list2 if i not in list1 or i not in list2]
        diff_list2 = [i for i in list1 + list3 if i not in list1 or i not in list3]
        diff_list = list(set(diff_list1 + diff_list2))

        #if not is_dumped:
        es_util = ElasticUtil()

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((addr, LIME_PORT))
            if len(diff_list2) == 0:
                s.send("No")
                s.close()
            else:
                s.send("Yes")
                s.close()
                # is_dumped = True
                recv_dump(addr)
        except:
            pass
        for module in diff_list:
            if not module:
                break
            inUser = False
            inKernel = False
            inSys = False
            if module in list1:
                inUser = True
            if module in list2:
                inKernel = True
            if module in list3:
                inSys = True
            doc = {"timestamp": datetime.utcnow(),
                   "IP": addr,
                   "KernelModules.ModuleName": module,
                   "inUser:": inUser,
                   "inKernel:": inKernel,
                   "inSys:": inSys}

            # Connection successful
            es_util.send_to_elastic("gymic-comparemodule", "ModulesCompare", doc)

    except Exception as e:
        es = ElasticUtil()
        es.log_error("CompareModule Error: " + e.message)


def searchForMiner(artifacts_list, addr):
    print "Miner finder"
    try:

        procs = artifacts_list["userProcess"].parsed_data
        net = artifacts_list["userNetwork"].parsed_data

        # Get process names for communicating processes
        netProcs = []
        for line in net:
            netProcs.append(line[-1])

        es_util = ElasticUtil()

        # Call model building method
        global mlModel
        global lableEncoderProc
        global lableEncoderUser
        if mlModel == None:
            created_model = minerMLMode_createModel()
            mlModel = created_model[0]
            lableEncoderProc = created_model[1]
            lableEncoderUser = created_model[2]

        # Inspect each process
        for proc in procs:
            if proc[2] != "":

                # Set communication value
                comm = 50 if proc[2] in netProcs else 0
                if minerMLMode_inspect(mlModel, lableEncoderProc, lableEncoderUser, proc, comm) == 1:
                    print "ML FOUND PROC : " + proc[2]
                    doc = {"timestamp": datetime.utcnow(),
                           "IP": addr,
                           "UserProcesses.PID": proc[0],
                           "UserProcesses.CPU": proc[1],
                           "UserProcesses.ProcessName": proc[2]}
                    es_util.send_to_elastic("gymic-miner", "MinerFinder", doc)

    except Exception as e:
        es = ElasticUtil()
        es.log_error("MinerFinder Error: " + e.message)
        print "Miner: " + e.message


