import os
import subprocess
from subprocess import Popen


def dump_schema(path="test.sql"):
    _dump_schema(
        os.environ['PGHOSTNAME'],
        os.environ['PGDATABASE'],
        os.environ['PGUSERNAME'],
        os.environ['PGPASSWORD'],
        os.environ['PGBACKUPPATH'] + path
    )


def _dump_schema(host, dbname, user, password, path, **kwargs):
    bd_docker_name = os.environ['DBDOCKERDBNAME']
    bd_docker_compose = os.environ['DBDOCKERLOCATION']

    docker_command_extension = ''
    if bd_docker_name is not None and bd_docker_name != "":
        docker_command_extension = f'docker compose ' \
                                   f'-f {bd_docker_compose} ' \
                                   f'exec {bd_docker_name} '
    process = subprocess.run(['pg_dump', '--dbname', dbname, '--username', user, '--host', host],
                             env={'PGPASSWORD' : password}
                             )
    # command =  f'{docker_command_extension}pg_dump --host={host} ' \
    #           f'--dbname={dbname} ' \
    #           f'--username={user} ' \
    #           f'--inserts ' \
    #           f'> {path} '
    # print(command)
    # proc = Popen(command, shell=False)
    # return proc.communicate(password)
