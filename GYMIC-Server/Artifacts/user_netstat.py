from datetime import datetime

from elastic_util import ElasticUtil

class UserNetstat:

    @staticmethod
    def parse_to_json(raw_data):
        parsed_user_connections = []
        raw_str = raw_data.strip("userNetworkActive Internet connections (servers and established)\nProto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name\n")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            line = " ".join(line.split())
            temp_line = line.split(" ")
            protocol = temp_line[0]
            temp_local_addr = temp_line[3].split(':')
            local_port = temp_local_addr[-1]
            if len(temp_local_addr) > 2:
                local_addr = "127.0.0.1"
            else:
                local_addr = temp_local_addr[0]
            temp_remote_addr = temp_line[4].split(':')
            remote_port = temp_remote_addr[-1]
            if len(temp_remote_addr) > 2:
                remote_addr = "127.0.0.1"
            else:
                remote_addr = temp_remote_addr[0]
            if len(temp_line) < 7:
                state = "UNKNOWN"
            else:
                state = temp_line[5]
            pid = '-'
            prog_name = '-'
            if not temp_line[-1].startswith('-'):
                pid = temp_line[-1].split('/')[0]
                prog_name = temp_line[-1].split('/')[-1]

            parsed_user_connections.append((protocol, local_addr, local_port, remote_addr, remote_port, state, pid, prog_name))
        return parsed_user_connections

    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:

                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "UserNetstat.Protocol": line[0],
                       "UserNetstat.LocalAddress": line[1],
                       "UserNetstat.LocalPort": line[2],
                       "UserNetstat.RemoteAddress": line[3],
                       "UserNetstat.RemotePort": line[4],
                       "UserNetstat.State": line[5],
                       "UserNetstat.PID": line[6],
                       "UserNetstat.ProgramName": line[-1]}

                # Connection successful
                es_util.send_to_elastic("gymic-usernetstat", "UserNetstat", doc)


            except Exception as e:

                # Connection unsuccessful.
                es_util.log_error("UserNetstat send error: " + e.message)
