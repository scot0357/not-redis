import abc
import shlex
import collections


COMMAND_REGISTRY = {}


def register_command(cls):
    for cmd in cls.get_public_commands():
        COMMAND_REGISTRY[cmd] = cls


def exec_command(cmdline, namespace_mgr):
    cmd, *args = shlex.split(cmdline)
    cleaned_cmd = cmd.lower()
    cls = COMMAND_REGISTRY[cleaned_cmd]

    namespace_name = cls.get_namespace_name()
    namespace = namespace_mgr.get_namespace(namespace_name)

    command = cls(namespace)
    method = getattr(command, cleaned_cmd)
    return method(*args)


class Command(abc.ABC):

    def __init__(self, namespace):
        self.namespace = namespace

    @abc.abstractmethod
    def evaluate(self, *args, **kwargs):
        """Take arguments passed on the command line to do something."""


class SingleCommand(Command):

    @classmethod
    def get_public_command(cls):
        return ['incr', 'set', 'exists', 'incrby']

    @classmethod
    def get_namespace_name(cls):
        return '__SINGLE'

    def set(self, varname, value):
        self.namespace[varname] = str(value)
        return "OK"


@register_command
class Set(Command, SingleMixin):

    def evaluate(self, varname, value):
        self.namespace[varname] = str(value)
        return "OK"


@register_command
class Exists(Command, SingleMixin):

    def evaluate(self, *keys):
        num_exists = sum([1 if str(x) in self.namespace
                          else 0
                          for x in keys])
        return "(integer) {}".format(num_exists)


@register_command
class Incr(Command, SingleMixin):

    def evaluate(self, key):
        current = self.namespace.get(key, "0")
        new = int(current) + 1
        num_exists = sum([1 if x in self.namespace
                          else 0
                          for x in keys])
        return "(integer) {}".format(num_exists)
