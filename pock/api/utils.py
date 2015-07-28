import subprocess

from pyquery import PyQuery as pq


def check_output(command):
    """Substitute for subprocess.check_output.

    Python 2.6 doesn't have subprocess.check_output, so we
    implement a basic substitute here.
    """

    return subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]


def get_cib():
    """Gets the current CIB.

    Returns a PyQuery object
    """

    return pq(check_output(['cibadmin', '--query', '--local']))


def update_cib(new_xml, parent=None):
    """Updates the CIB."""

    cib = get_cib()

    cib.find(parent).append(new_xml)

    p = subprocess.Popen(['cibadmin', '--replace', '--xml-pipe'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    stdout = p.communicate(input=cib.html())[0]

    return stdout



def crm_mon():
    """Gets the output from crm_mon."""

    return check_output(['crm_mon', '-1', '-r'])


def get_state(res_id):
    """Gets the current state of a resource.

    Calls crm_mon to get current state, then looks for an id in
    the stdout that matches `res_id`. Returns None if the id
    cannot be found, otherwise returns a string representing the
    current state of the resource. Some examples are `Started`
    and `Stopped`.
    """

    lines = crm_mon().split('\n')

    try:
        line = [l for l in lines if l.startswith(' %s\t' % res_id)][0]
    except IndexError:
        return None

    return line.split('\t')[-1].split(' ')[0]
