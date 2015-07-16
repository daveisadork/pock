import subprocess

from pyquery import PyQuery as pq


def cibadmin(command):
    response = subprocess.check_output(command)
    return pq(response)
