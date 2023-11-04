import os
import subprocess
import time
from subprocess import Popen, PIPE

import pexpect


def dump_schema(path="test.sql"):
    _dump_schema(
        os.environ['PGHOSTNAME'],
        os.environ['PGDATABASE'],
        os.environ['PGUSERNAME'],
        os.environ['PGPASSWORD'],
        path
    )


def _dump_schema(host, dbname, user, password, path, **kwargs):
    # subprocess.call(['sh', './test.sh'])
    bd_docker_name = os.environ['DBDOCKERDBNAME']
    bd_docker_compose = os.environ['DBDOCKERLOCATION']
    print('Создание бекапа')
    os.makedirs('./backups', exist_ok=True)
    execute_command(f'docker compose -f {bd_docker_compose} exec {bd_docker_name} mkdir -p backups')

    child = pexpect.spawn(
        f'docker compose -f {bd_docker_compose} '
        f'exec {bd_docker_name} '
        f'pg_dump -U {user} '
        f'-h {host}'
        f' -Ft {dbname} '
        f' -f backups/{path}')
    time.sleep(1)
    password += "\n"
    child.sendline(password)

    execute_command(
        f'docker compose -f {bd_docker_compose} cp {bd_docker_name}:/backups/{path} backups/{path}')
    execute_command(f'docker compose -f {bd_docker_compose} exec {bd_docker_name} rm backups/{path}')
    print('Бекап создан', f'backups/{path}')
    return

    # command = f'pg_dump --host={host} ' \
    #           f'--dbname={dbname} ' \
    #           f'--username={user} ' \
    #           f'--inserts ' \
    #           f'--file=/tmp/schema.dmp ' \
    #           f'> {path} '
    # print(command)
    # proc = Popen(command, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    # return proc.communicate(password)


def execute_command(command):
    proc = Popen(command, shell=True)
    res = proc.wait()
    if res:
        raise
    return proc


def execute_command_with_result(command):
    proc = Popen(command, shell=True)
    return proc
