from conf import ELK_SERVER_IP, ELK_SERVER_PORT
import json
from elasticsearch import Elasticsearch
from Artifacts import UserThreads

class Artifact:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.parsed_data = ""

        if raw_data.startswith("userThreads"): self.artifact_type = UserThreads
        else: self.artifact_type = None



    def parse_to_json(self):
        if self.artifact_type is not None:
            self.parsed_data = self.artifact_type.parse_to_json(self.raw_data)
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
            self.artifact_type.send_to_elastic(self.parsed_data)

    def append_data(self, new_data):
        self.raw_data += new_data
