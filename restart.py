import os
from subprocess import Popen


def restart_db():
    bd_docker_name = os.environ['DBDOCKERDBNAME']
    bd_docker_compose = os.environ['DBDOCKERLOCATION']

    command = f'docker compose restart ' \
              f'-f {bd_docker_compose} ' \
              f'{bd_docker_name}'

    proc = Popen(command, shell=True, )
    status = proc.wait()
    if status:
        raise Exception('Error while restart')