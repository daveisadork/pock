import subprocess

from pyquery import PyQuery as pq


def check_output(command):
    return subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]


def cibadmin(command):
    return pq(check_output(command))


def crm_mon():
    return check_output(['crm_mon', '-1', '-r'])


def get_state(res_id):
    lines = crm_mon().split('\n')

    try:
        line = [l for l in lines if l.startswith(' %s\t' % res_id)][0]
    except IndexError:
        return None

    return line.split('\t')[-1].split(' ')[0]
