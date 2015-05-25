# Wharf-Rat

A simple tool to translate yml config files into docker commands.

## Install

pip install wharfrat

## Basics

Wharf-Rat lets you configure your Docker commands in a yml file.  The file
is a list of data objects, instances and tasks.

An instance maps directly to a single docker run command.  It will specify
what docker instance to run, along with all the options like environment
variables and volumes.

A task is a set of instances that are run together.  The only currently
implemented scheme is a basic task command.  This stands up a list of
dependent instances daemonized, and then launches one instance in the
foreground.  When this instance exits it and all of the dependant containers
are cleaned up (docker rm -fv).  

## Tasks

```
test:
  type: task
  primary: webapp
  images:
    - redis
    - mysql
    - postgres
    - celeryd
```

This creates a task with the name "test".  The containers in primary and images
must be specified by name elsewhere in the file.  Images are started with
`docker run -d ...`.  The primary is run with `docker run --rm`.  

## Instances

```
webapp:
  type: instance
  image: busybox
  links:
    - redis:redis
    - mysql:mysql
  environment:
    - ENV=local
    - PYTHONPATH=/data
  volumes:
    - .:/data
  workdir: /data
  entrypoint: python
  command: setup.py test
```

This is an instance named "webapp".  It uses the image "busybox".  You can also
give it a command `build: mydir` which will cause it to run `docker build mydir`
and use the resultant image.  

## Running a task

`wharfrat -f <CONFIG_FILE.yml> run <MY_TASK>`

If you don't specify a config file, it will look for "wharfrat.yml" in the
current working directory.  <MY_TASK> is the name of the task to run.

# Develop

virtualenv -p python2.7 venv
source venv/bin/activate
python setup.py develop
python setup.py test

## Run docker on OSX
    $ brew install docker
    $ brew install boot2docker
    $ boot2docker init
    $ boot2docker up

(copy the three `export` commands that `boot2docker` outputs into your `~/.profile` or similar file)
