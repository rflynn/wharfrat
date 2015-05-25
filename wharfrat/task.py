from wharfrat.container import TaskContainer


class Task():

    def __init__(self, name, data, containers):
        self.name = name
        container_names = data.get('images', [])
        self.containers = [TaskContainer(containers[_name], self)
                           for _name in container_names]
        self.primary = TaskContainer(containers[data['primary']],
                                     self, remove=True) if \
            data.get('primary') else None

    def run(self):
        commands = []
        for x in self.containers:
            if x.get_setup_command():
                commands.append(x.get_setup_command())
        if self.primary:
            if self.primary.get_setup_command():
                commands.append(self.primary.get_setup_command())
        for x in self.containers:
            commands.append(x.get_run_command())
        if self.primary:
            commands.append(self.primary.get_run_command())
        for x in self.containers:
            commands.append(x.get_cleanup_command())
        return commands
