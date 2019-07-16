from datetime import datetime

from elastic_util import ElasticUtil

# Dedicated Class for kernel mode modules
class KernelModules:

    # Parse kernel mode modules data
    @staticmethod
    def parse_to_json(raw_data):
        parsed_kernel_modules = []
        raw_str = raw_data.strip("kernelModulesmodules\n")
        raw_lines = raw_str.split("\n")
        for line in raw_lines:
            temp_line=line.strip(" ")
            if temp_line != None:
                parsed_kernel_modules.append(temp_line)
        return parsed_kernel_modules

    # Send parsed modules to elastic
    @staticmethod
    def send_to_elastic(parsed_data, addr):
        es_util = ElasticUtil()
        for line in parsed_data:

            try:

                doc = {"timestamp": datetime.utcnow(),
                       "IP": addr,
                       "KernelModules.ModuleName": line}

                # Connection successful
                es_util.send_to_elastic("gymic-kernelmodules", "KernelModules", doc)


            except Exception as e:

                # Connection unsuccessful.
                es_util.log_error("KernelModules send error: " + e.message)
