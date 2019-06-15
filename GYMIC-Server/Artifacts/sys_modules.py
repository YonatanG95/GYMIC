from datetime import datetime

from elastic_util import ElasticUtil

class SysModules:

    @staticmethod
    def parse_to_json(raw_data):
        parsed_sys_modules = []
        raw_str = raw_data.strip("sysModule\n")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line=line.strip(" ")
            if temp_line != None:
                parsed_sys_modules.append(temp_line)
        return parsed_sys_modules

    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:

                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "SysModules.ModuleName": line}

                # Connection successful
                es_util.send_to_elastic("gymic-sysmodules", "SysModules", doc)

            except Exception as e:

                # Connection unsuccessful.
                es_util.log_error("SysModules send error: " + e.message)
