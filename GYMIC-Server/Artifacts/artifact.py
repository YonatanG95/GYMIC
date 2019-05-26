from elastic_util import ElasticUtil
from user_threads import UserThreads
from kernel_threads import KernelThreads
from user_processes import UserProcesses
from kernel_processes import KernelProcesses
from user_netstat import UserNetstat
from user_modules import UserModules
from kernel_modules import KernelModules

class Artifact:
    def __init__(self, raw_data, addr):
        self.addr = addr
        self.raw_data = raw_data
        self.parsed_data = ""

        if raw_data.startswith("userThreads"):
            self.artifact_type = UserThreads
            self.artifact_header = "userThreads"
        elif raw_data.startswith("kernelThreads"):
            self.artifact_type = KernelThreads
            self.artifact_header = "kernelThreads"
        elif raw_data.startswith("userProcess"):
            self.artifact_type = UserProcesses
            self.artifact_header = "userProcess"
        elif raw_data.startswith("kernelProcesses"):
            self.artifact_type = KernelProcesses
            self.artifact_header = "kernelProcesses"
        elif raw_data.startswith("userNetwork"):
            self.artifact_type = UserNetstat
            self.artifact_header = "userNetwork"
        elif raw_data.startswith("userModule"):
            self.artifact_type = UserModules
            self.artifact_header = "userModule"
        elif raw_data.startswith("kernelModule"):
            self.artifact_type = KernelModules
            self.artifact_header = "kernelModule"
        else: self.artifact_type = None



    def parse_to_json(self):
        if self.artifact_type is not None:
            try:
                self.parsed_data = self.artifact_type.parse_to_json(self.raw_data)
            except Exception as e:
                es = ElasticUtil()
                es.log_error("ParseError: " + e.message)
        """
        processes = []
        processes = self.raw_data['data'].split("\n")
        print "first split worked"
        for i in xrange(0, len(processes)-1, 1):
            processes[i] = tuple(processes[i].split(" "))
        print "second split worked"
        print processes
        del rs[0]
        rs = json.dumps(dict(processes))
        #self.raw_data['data'] = processes
        #rs = json.dumps(self.raw_data)
        self.parsed_data = rs
        print "json dumps worked"
        """
        

    def send_to_elastic(self):
        if self.artifact_type is not None:
            self.artifact_type.send_to_elastic(self.parsed_data, self.addr)

    def append_data(self, new_data):
        self.raw_data += new_data
