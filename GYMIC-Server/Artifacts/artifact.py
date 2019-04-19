from elastic_util import ElasticUtil
from user_threads import UserThreads
from kernel_threads import KernelThreads
from user_processes import UserProcesses
from kernel_processes import KernelProcesses

class Artifact:
    def __init__(self, raw_data, addr):
        self.addr = addr
        self.raw_data = raw_data
        self.parsed_data = ""

        if raw_data.startswith("userThreads"): self.artifact_type = UserThreads
        elif raw_data.startswith("kernelThreads"): self.artifact_type = KernelThreads
        elif raw_data.startswith("userProcess"): self.artifact_type = UserProcesses
        elif raw_data.startswith("kernelProcesses"): self.artifact_type = KernelProcesses
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
