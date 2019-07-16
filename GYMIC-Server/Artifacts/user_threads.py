from datetime import datetime

from elastic_util import ElasticUtil

# Dedicated Class for user mode threads
class UserThreads:

    # Parse user mode threads data
    @staticmethod
    def parse_to_json(raw_data):
        parsed_user_threads = []
        raw_str = raw_data.strip("userThreadsPID SPID\n")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line=line.split(" ", 1)
            if temp_line[-1] != None:
                parsed_user_threads.append((temp_line[0],temp_line[-1]))
        return parsed_user_threads

    # Send parsed threads to elastic
    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:

                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "UserThreads.TID": line[-1],
                       "UserThreads.PID": line[0]}

                # Connection successful
                es_util.send_to_elastic("gymic-userthreads", "UserThreads", doc)


            except Exception as e:

                # Connection unsuccessful.
                es_util.log_error("UserThreads send error: " + e.message)
