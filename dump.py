import os
from subprocess import Popen


def dump_schema(path):
    _dump_schema(
        os.environ['PGHOSTNAME'],
        os.environ['PGDATABASE'],
        os.environ['PGUSERNAME'],
        os.environ['PGPASSWORD'],
        os.environ['PGBACKUPPATH'] + path
    )


def _dump_schema(host, dbname, user, password, path, **kwargs):
    bd_docker_name = os.environ['DBDOCKERNAME']
    docker_command_extension = ''
    if bd_docker_name is not None and bd_docker_name != "":
        docker_command_extension = f'docker exec {bd_docker_name} /usr/bin/'
    command = f'{docker_command_extension}pg_dump --host={host} ' \
              f'--dbname={dbname} ' \
              f'--username={user} ' \
              f'> {path} '
    print(command)
    proc = Popen(command, shell=True, env={
        'PGPASSWORD': password
    })
    return proc.communicate(password)

