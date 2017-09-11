import abc
import collections


COMMAND_REGISTRY = {}


def register_command(cls):
    COMMAND_REGISTRY[cls.__name__] = cls


namespace = collections.defaultdict(dict)


class Command(abc.ABC):

    @abc.abstractmethod
    def evaluate(self, *args, **kwargs):
        """Take arguments passed on the command line to do somehting."""

    @abc.abstractproperty
    def namespace(self):
        """The associated namespace the command is associated with."""


class Set(Command):

    def namespace(self):
        return namespace['numeric']
        return 'numeric'

    def evaluate(self, varname, value):
        self.namespace[varname] = value
        return "OK"


class Exists(Command):

    def namespace(self):
        return namespace['numeric']

    def evaluate(self, *keys):
        return sum([1 if x in self.namespace else 0 for x in keys])
