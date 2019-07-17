from datetime import datetime

from elastic_util import ElasticUtil

# Dedicated Class for kernel mode processes
class KernelProcesses:

    # Parse kernel mode processes data
    @staticmethod
    def parse_to_json(raw_data):
        parsed_kernel_processes = []
        raw_str = raw_data.strip("kernelProcessesprocesses\n")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line=line.split(" ", 1)
            if temp_line[-1] != None:
                parsed_kernel_processes.append((temp_line[0],temp_line[-1]))
        return parsed_kernel_processes

    # Send parsed processes to elastic
    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:

                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "KernelProccesess.PID": line[0],
                       "KernelProcesses.ProcessName": line[-1]}

                # Connection successful
                es_util.send_to_elastic("gymic-kernelprocesses", "KernelProcesses", doc)


            except Exception as e:
                # Connection unsuccessful.
                es_util.log_error("KernelProcesses send error: " + e.message)
