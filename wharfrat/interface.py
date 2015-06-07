from subprocess import check_output, STDOUT, CalledProcessError
import sys

def issue(command):
    try:
        response = check_output(command, stderr=STDOUT, shell=True)
    except CalledProcessError as e:
        print e.output
        raise e
    print response
    return response
