import os
import yaml

from wharfrat.container import Container
from wharfrat.task import Task


class WharfRat():

    def __init__(self, data, directory=os.getcwd()):

        self.instances = {x: Container(x, data[x], directory) for x in data
                          if data[x]['type'] == 'instance'}

        self.tasks = {x: Task(x, data[x], self.instances) for x in data
                      if data[x]['type'] == 'task'}

    @classmethod
    def build(cls, args):
        filename = 'wharfrat.yml'
        if args.filename:
            filename = args.filename
        directory = os.path.dirname(os.path.abspath(filename))
        return cls(cls._load(filename), directory)

    @staticmethod
    def _load(filename):
        with open(filename, 'r') as f:
            return yaml.load(f)


    def run(self, task):

        return self.tasks[task].run()
