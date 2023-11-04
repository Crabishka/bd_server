import os
import subprocess
import time
from datetime import datetime
from email.utils import format_datetime
from subprocess import Popen, PIPE

import pexpect


def format_datetime(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')


def get_dumps():
    # заменить на .env
    path = './backups'
    result = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        file_stat = os.stat(file_path)
        file_name = os.path.splitext(filename)[0]
        file_size = file_stat.st_size
        file_datetime = format_datetime(file_stat.st_ctime)
        file_info = {"name": file_name, "datetime": file_datetime, "size" : file_size}
        print(file_info)
        result.append(file_info)
    return result


def dump_schema(path="test.sql"):
    _dump_schema(
        os.environ['PGHOSTNAME'],
        os.environ['PGDATABASE'],
        os.environ['PGUSERNAME'],
        os.environ['PGPASSWORD'],
        path
    )


def restore_schema(path="test.sql"):
    _restore_schema(
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

    command = f'docker compose -f {bd_docker_compose} ' \
              f'exec {bd_docker_name} ' \
              f'pg_dump -U {user} ' \
              f'-h {host}' \
              f' -Ft {dbname} ' \
              f' -f backups/{path}'
    print(command, "\n")
    child = pexpect.spawn(command)
    time.sleep(1)
    password += "\n"
    child.sendline(password)
    child.wait()

    command = f'docker compose -f {bd_docker_compose} cp {bd_docker_name}:/backups/{path} ./backups'
    print(command)
    execute_command(command)
    # execute_command(f'docker compose -f {bd_docker_compose} exec {bd_docker_name}  backups/{path}')
    print('Бекап создан', f'backups/{path}')
    return


def _restore_schema(host, dbname, user, password, path, **kwargs):
    bd_docker_name = os.environ['DBDOCKERDBNAME']
    bd_docker_compose = os.environ['DBDOCKERLOCATION']
    print(f'Восстановление бекапа {path}')
    command = f'docker compose -f {bd_docker_compose} cp ./backups/{path} {bd_docker_name}:/backups'
    execute_command(command)

    command = f'docker compose -f {bd_docker_compose} ' \
              f'exec {bd_docker_name} ' \
              f'pg_restore -U {user} ' \
              f'-h {host} ' \
              f'-d {dbname}' \
              f' backups/{path}'
    print(command, "\n")
    child = pexpect.spawn(command)
    time.sleep(1)
    password += "\n"
    child.sendline(password)
    child.wait()
    print(f'Бекап {path} восстановлен')


def execute_command(command):
    proc = Popen(command, shell=True)
    res = proc.wait()
    if res:
        raise
    return proc


def execute_command_with_result(command):
    proc = Popen(command, shell=True)
    return proc
