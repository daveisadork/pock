import subprocess

from pyquery import PyQuery as pq


class ResourceManager():
    def list(self):
        response = subprocess.check_output(['cibadmin', '--query', '--local'])
        print(response)
        xml = pq(response)
        print(xml)
