from datetime import datetime

from elastic_util import ElasticUtil

class UserProcesses:

    @staticmethod
    def parse_to_json(raw_data):
        parsed_user_processes = []
        raw_str = raw_data.strip("userProcessPID %CPU COMMAND\n").strip("<defunct>")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line=line.split(" ")
            name = temp_line[2]
            cpu = float(temp_line[1])
            pid = temp_line[0]
            if name is not None:
                parsed_user_processes.append((pid, cpu, name))
        return parsed_user_processes

    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:
                name = line[-1]
                cpu = line[-2]
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
