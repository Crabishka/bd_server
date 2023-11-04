import json
import os
from subprocess import Popen


def get_hardware_utils():
    db_docker_name = os.environ['DBDOCKERDBNAME']
    command = f'docker stats --no-stream --format   "{{{{ json . }}}}"  {db_docker_name}'
    proc = Popen(f'{command} > tmp', shell=True)
    proc.wait()
    data = open('tmp', 'r').read()
    print(data)
    if data != "":
        hardware_data = json.loads(data)
        return hardware_data
    return {}

