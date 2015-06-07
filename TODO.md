This is a list of features I need for Wharfrat to accomplish the goal of 
replacing my day to day bash scripts-

#  Templating

Many of my bash scripts right now have to do things like replace
`image: myorg/myimage:{{version}}` with `image: myorg/myimage:3fsa23cwasd`.  I
am working on using Jinja2 to replace template variables in the wharfrat.yml
file.  I am not sure the best way to do this yet, currently I am thinking that
each task could have default values to override variables set on the containers,
which could be overridden on the command line.

# Command Issuer

The command line output currently blocks.  It should flow instead.

# Committing

I have tasks that start up some linked containers, run tasks, and then commit
some of the results as images.  I would like to have a wharfrat task to do this.

# Services

Right now the only task format is to launch linked containers, run a command in
a foreground container, and then remove all of the containers.  I need to be
able to run a traditional 'docker-compose up' type of command as well

# Pull

I need a command to pull relevant containers before running other commands.  It
would also be nice to have an option to set 'auto pull' on some tasks.
