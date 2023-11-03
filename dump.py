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

    command = f'pg_dump --host={host} ' \
              f'--dbname={dbname} ' \
              f'--username={user} ' \
              f'--no-password ' \
              f'--file={path} '

    proc = Popen(command, shell=True, env={
        'PGPASSWORD': password
    })
    proc.wait()


