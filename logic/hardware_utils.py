import json
import os
from subprocess import Popen


def get_hardware_utils():
    db_docker_name = os.environ['DBDOCKERDBNAME']
    command = f'docker stats --no-stream --format   "{{{{ json . }}}}"  app'
    proc = Popen(f'{command} > tmp', shell=True)
    proc.wait()
    data = open('tmp', 'r').read()
    if data != "":
        hardware_data = json.loads(data)
        print(hardware_data)
        return hardware_data
    return {}

