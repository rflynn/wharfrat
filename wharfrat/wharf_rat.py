from wharfrat.container import Container
from wharfrat.task import Task


class WharfRat():

    def __init__(self, data):

        self.instances = {x: Container(x, data[x]) for x in data
                          if data[x]['type'] == 'instance'}

        self.tasks = {x: Task(x, data[x], self.instances) for x in data
                      if data[x]['type'] == 'task'}

    def run(self, task):

        return self.tasks[task].run()
