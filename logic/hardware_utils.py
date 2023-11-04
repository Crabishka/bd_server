import json
import os


def get_hardware_utils():
    db_name = os.environ['PGDATABASE']
    command = f'docker stats --no-stream --format   "{{ json . }}"  {db_name}'
    os.system(f'{command} > tmp')
    data = open('tmp', 'r').read()
    hardware_data = json.loads(data)
    return hardware_data

