import socket
import os
from datetime import datetime

from conf import LIME_PORT
from elastic_util import ElasticUtil

def recv_dump(ip):

    try:
        output_dir = os.path.join(os.getcwd(), 'Dumps')
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        output_path = os.path.join(output_dir, datetime.now().strftime("%Y-%m-%d %H-%M-%S") + " - " + ip + ".lime")
        with open(output_path, 'wb') as out:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, LIME_PORT))
            except Exception as e:
                es = ElasticUtil()
                es.log_error("DumpReceive ConnectError: " + e.message)
            while True:
                mem_data = s.recv(1024)
                if not mem_data:
                    break
                out.write(mem_data)

        es = ElasticUtil()
        es.log("Successfully dumped memory to " + output_path)

    except Exception as e:
        es = ElasticUtil()
        es.log_error("DumpReceive CreateError: " + e.message)




