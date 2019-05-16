from datetime import datetime

from elastic_util import ElasticUtil

class UserProcesses:

    @staticmethod
    def parse_to_json(raw_data):
        parsed_user_processes = []
        raw_str = raw_data.strip("userProcessPID COMMAND\n")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line=line.split(" ", 1)
            if temp_line[-1] != None:
                parsed_user_processes.append((temp_line[0],temp_line[-1]))
        return parsed_user_processes

    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:
            # print " --> " + line[-1]
            try:
                name = line[-1].split(" ")[1]
                cpu = line[-1].split(" ")[0]
                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "UserProccesess.PID": line[0],
                       "UserProcesses.ProcessName": name,
                       "UserProcesses.CPU": cpu}

                # Connection successful
                es_util.send_to_elastic("gymic-userprocesses", "UserProcesses", doc)


            except Exception as e:
                # Connection unsuccessful.
                es_util.log_error("UserProcesses send error: " + e.message)
