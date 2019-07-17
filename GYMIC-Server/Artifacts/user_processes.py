from datetime import datetime

from elastic_util import ElasticUtil

# Dedicated Class for user mode processes
class UserProcesses:

    # Parse user mode processes data
    @staticmethod
    def parse_to_json(raw_data):
        parsed_user_processes = []
        raw_str = raw_data.strip("userProcessPID %CPU COMMAND USER\n").replace("<defunct>", "")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line = (" ".join(line.split())).split(" ")
            if len(temp_line) > 3:
                #print temp_line
                name = temp_line[2]
                cpu = float(temp_line[1])
                pid = temp_line[0]
                user = temp_line[3]
                if name is not None:
                    parsed_user_processes.append((pid, cpu, name, user))
        return parsed_user_processes

    # Send parsed processes to elastic
    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:
                pid = line[0]
                name = line[2]
                cpu = line[1]
                user = line[3]
                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "UserProccesess.PID": pid,
                       "UserProcesses.ProcessName": name,
                       "UserProcesses.CPU": cpu,
                       "UserProcesses.USER": user}

                # Connection successful
                es_util.send_to_elastic("gymic-userprocesses", "UserProcesses", doc)

            except Exception as e:
                # Connection unsuccessful.
                es_util.log_error("UserProcesses send error: " + e.message)
