from subprocess import Popen, STDOUT, PIPE, CalledProcessError
import sys

# FIXME: not portable
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK
from select import select
import errno

def issue(command):
    try:
        p = Popen(command,
                  stdout=PIPE,
                  stderr=PIPE,
                  shell=True)
        response = handle_output(p)
        e = p.returncode
        if e:
            raise CalledProcessError(e, command, output=response)
    except CalledProcessError as e:
        print e.output
        raise e
    try:
        p.close()
    except:
        pass
    return response

def handle_output(p):

    def unblock_file(f):
        flags = fcntl(f, F_GETFL)
        fcntl(f, F_SETFL, flags | O_NONBLOCK)

    response = []
    try:
        unblock_file(p.stdout)
        unblock_file(p.stderr)
        exitcode = p.poll()
        while exitcode is None:
            readable, _, _ = select([p.stdout, p.stderr], [], [], 0.125)
            for r in readable:
                try:
                    x = r.read()
                    response.append(x)
                    sys.stdout.write(x)
                except: pass
            exitcode = p.poll()
    except:
        raise
    return ''.join(response)
