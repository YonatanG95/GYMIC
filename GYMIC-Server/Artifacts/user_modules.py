from datetime import datetime

from elastic_util import ElasticUtil

class UserModules:

    @staticmethod
    def parse_to_json(raw_data):
        parsed_user_modules = []
        raw_str = raw_data.strip("userModuleModule                  Size  Used by\n")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line=line.split(" ", 1)
            if temp_line[0] != None:
                parsed_user_modules.append(temp_line[0])
        return parsed_user_modules

    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:

                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "UserModules.ModuleName": line}

                # Connection successful
                es_util.send_to_elastic("gymic-usermodules", "UserModules", doc)


            except Exception as e:

                # Connection unsuccessful.
                es_util.log_error("UserModules send error: " + e.message)
