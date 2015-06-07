from subprocess import Popen, STDOUT, PIPE, CalledProcessError
import sys


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
    return response


def handle_output(p):
    response = []
    try:
        c = p.communicate()
        while c:
            out, err = c
            if out:
                response.append(out)
                sys.stdout.write(out)
            if err:
                response.append(err)
                sys.stderr.write(err)
            c = p.communicate()
    except ValueError as e:
        pass # .communicate() on dead process, it's fine...
    return ''.join(response)
