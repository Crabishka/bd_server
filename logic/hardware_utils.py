import json
import os
from subprocess import Popen


def get_hardware_utils():
    db_name = os.environ['PGDATABASE']
    command = f'docker stats --no-stream --format   "{{ json . }}"  {db_name}'
    proc = Popen(f'{command} > tmp')
    proc.wait()
    data = open('tmp', 'r').read()
    print(data)
    if data != "":
        hardware_data = json.loads(data)
        return hardware_data
    return {}

