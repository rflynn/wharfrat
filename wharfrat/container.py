import os


class Container():

    def __init__(self, name, data, directory):
        self.name = name
        self.directory = directory
        self.image = data.get('image')
        self.build = data.get('build')
        if self.build and not os.path.isabs(self.build):
            self.build = os.path.join(directory, self.build)
        self.dockerfile = data.get('dockerfile')
        if self.dockerfile and not os.path.isabs(self.dockerfile):
            self.dockerfile = os.path.join(directory, self.dockerfile)
        self.links = [l for l in data.get('links', [])]
        self.volumes = [v for v in data.get('volumes', [])]
        self.volumes_from = [vf for vf in data.get('volumes-from', [])]
        self.ports = [p for p in data.get('ports', [])]
        self.environment = [e for e in data.get('environment', [])]
        self.entrypoint = data.get('entrypoint')
        self.command = data.get('command')

    def get_run_command(self, task, remove=False):

        options = ['--name %s-%s' % (task, self.name)]
        for l in self.links:
            options.append('--link %s-%s' % (task, l))
        for v in self.volumes:
            if not os.path.isabs(v.split(':')[0]):
                first, last = v.split(':', 1)
                first = os.path.join(self.directory, first)
                v = first + ':' + last
            options.append('-v %s' % v)
        for vf in self.volumes_from:
            options.append('--volumes-from %s' % vf)
        for p in self.ports:
            options.append('-p %s' % p)
        for e in self.environment:
            options.append('-e %s' % e)
        if self.entrypoint:
            options.append('--entrypoint %s' % self.entrypoint)
        if remove:
            options.append('--rm')
        else:
            options.append('-d')
        options.append(self.image)
        if self.command:
            options.append(self.command)
        return 'docker run %s' % ' '.join(options)

    def get_cleanup_command(self, task):

        return 'docker rm -fv %s-%s' % (task, self.name)

    def get_setup_command(self, task):

        self.image = '%s/%s' % (task, self.name)
        command = self.image
        if self.dockerfile:
            command = self.image + ' -f %s' % self.dockerfile
        return 'docker build -t %s %s' % (command, self.build)


class TaskContainer():

    def __init__(self, container, task, remove=False):
        self.task_name = task.name
        self.container = container
        self.remove = remove

    def get_setup_command(self):
        if self.container.build:
            return self.container.get_setup_command(self.task_name)
        else:
            return None

    def get_run_command(self):
        return self.container.get_run_command(self.task_name, remove=self.remove)

    def get_cleanup_command(self):
        return self.container.get_cleanup_command(self.task_name)
