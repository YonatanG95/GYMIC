from datetime import datetime

from elastic_util import ElasticUtil

class KernelThreads:

    @staticmethod
    def parse_to_json(raw_data):
        parsed_kernel_threads = []
        raw_str = raw_data.strip("kernelThreadsthreads")
        raw_lines = raw_str.split(",")
        for line in raw_lines:
            temp_line=line.split(" ", 1)
            if temp_line[-1] != None:
                parsed_kernel_threads.append((temp_line[0],temp_line[-1]))
        return parsed_kernel_threads

    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:

                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "KernelThreads.TID": line[-1],
                       "KernelThreads.PID": line[0]}

                # Connection successful
                es_util.send_to_elastic("gymic-kernelthreads", "KernelThreads", doc)


            except Exception as e:

                # Connection unsuccessful.
                es_util.log_error("KernelThreads send error: " + e.message)