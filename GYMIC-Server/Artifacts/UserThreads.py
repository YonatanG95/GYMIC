from elasticsearch import Elasticsearch
from conf import ELK_SERVER_IP, ELK_SERVER_PORT


class UserThreads:

    @staticmethod
    def parse_to_json(raw_data):
        parsed_user_threads = []
        raw_str = raw_data.strip("userThreadsPID SPID\n")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line=line.split(" ")
            if temp_line[-1] != None:
                parsed_user_threads.append((temp_line[0],temp_line[-1]))
        return parsed_user_threads

    @staticmethod
    def send_to_elastic(parsed_data):
        es = Elasticsearch([{'host': ELK_SERVER_IP, 'port': ELK_SERVER_PORT}])
        for line in parsed_data:

            try:
                # Connection successful
                res = es.index(index="gymic-UserThreads", doc_type="UserThreads", body={"UserThreads.TID": line[-1], "UserThreads.PID": line[0]})


            except Exception as e:
                # Connection unsuccessful.
                print e.message
