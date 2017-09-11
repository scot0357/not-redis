import shlex
import traceback
from returntype import IntegerType, StrType, ErrorType, ListType
from datatype import SortedSet


COMMAND_REGISTRY = {}


def register_command(cls):
    for cmd in cls.get_public_commands():
        print(cmd)
        COMMAND_REGISTRY[cmd] = cls


def parse_cmdline(command):
    return shlex.split(command)


def exec_command(cmdline, namespace_mgr):
    try:
        cmd, *args = parse_cmdline(cmdline)
        cleaned_cmd = cmd.lower()
        cls = COMMAND_REGISTRY[cleaned_cmd]

        namespace_name = cls.get_namespace_name()
        namespace = namespace_mgr.get_namespace(namespace_name)

        command = cls(namespace)
        method = getattr(command, cleaned_cmd)
        ret = method(*args)
        return str(ret)
    except Exception as exc:
        traceback.print_exc()
        return str(ErrorType("Encountered exception: {}".format(exc)))


class Command:

    def __init__(self, namespace):
        self.namespace = namespace


@register_command
class SingleCommand(Command):

    @classmethod
    def get_public_commands(cls):
        return ['incr', 'set', 'exists', 'incrby', 'get']

    @classmethod
    def get_namespace_name(cls):
        return '__SINGLE'

    def set(self, varname, value):
        self.namespace[varname] = str(value)
        return StrType("OK")

    def get(self, key):
        return self.namespace.get(key, "(nil)")
        return StrType(key)

    def exists(self, *keys):
        num_exists = sum([1 if str(x) in self.namespace
                          else 0
                          for x in keys])
        return IntegerType(num_exists)

    def incr(self, key):
        try:
            value = int(self.namespace.get(key, 0))
        except (TypeError, ValueError):
            return ErrorType("value is not an integer or out of range")
        self.namespace[key] = str(value + 1)
        return IntegerType(self.namespace[key])

    def incrby(self, key, amount):
        try:
            amount = int(amount)
            value = int(self.namespace.get(key, 0))
        except (TypeError, ValueError):
            return ErrorType("value is not an integer or out of range")

        self.namespace[key] = str(value + amount)
        return IntegerType(self.namespace[key])


@register_command
class ListCommand(Command):

    @classmethod
    def get_public_commands(cls):
        return ['lpush', 'lpop', 'llen', 'lrem', 'lprint', 'lset']

    @classmethod
    def get_namespace_name(cls):
        return '__LIST'

    def lpush(self, key, *args):
        if not len(args):
            return get_error("wrong number of arguments for 'lpush' command")
        if key not in self.namespace:
            self.namespace[key] = []
        self.namespace[key].extend(args)
        return IntegerType(len(self.namespace[key]))

    def lpop(self, key):
        if key not in self.namespace or not self.namespace[key]:
            return StrType(None)

        return StrType(self.namespace[key].pop())

    def llen(self, key):
        if key not in self.namespace:
            return IntegerType(0)
        return IntegerType(len(self.namespace[key]))

    def lrem(self, key, count, value=None):
        if value is None:
            return IntegerType(0)

        try:
            count = int(count)
        except (TypeError, ValueError):
            return ErrorType("value is not an integer or out of range")

        # Have to make a copy and reassign to maintain big-O
        old_list = self.namespace.get(key, [])
        new_list = []

        if count < 0:
            for item in reversed(old_list):
                print(count)
                if str(item) != str(value) or count == 0:
                    new_list.append(item)
                else:
                    count += 1
        else:
            for item in old_list:
                print('i', item, 'value', value)
                if str(item) != str(value) or count == 0:
                    new_list.append(item)
                else:
                    count -= 1

        self.namespace[key] = new_list
        return IntegerType(len(self.namespace[key]))

    def lprint(self, key):
        return StrType(self.namespace.get(key))

    def lset(self, key, index, value):
        try:
            index = int(index)
        except (ValueError, TypeError):
            return ErrorType("value is not an integer or out of range")

        try:
            self.namespace[key][index] = value
        except IndexError:
            return ErrorType("index out of range")
        except KeyError:
            return ErrorType("no such key")
        return StrType("OK")


@register_command
class SortedSetCommand(Command):

    @classmethod
    def get_public_commands(cls):
        return ['zadd', 'zrem', 'zcard', 'zcount', 'zrank', 'zrange']

    @classmethod
    def get_namespace_name(cls):
        return '__SORTED_SET'

    def zadd(self, zkey, *pairs):
        if len(pairs) % 2 != 0:
            return ErrorType("invalid number of pairs")

        rest = pairs
        inserted = 0
        while rest:
            key, value, *rest = rest

            key = int(key)
            if zkey not in self.namespace:
                self.namespace[zkey] = SortedSet()

            self.namespace[zkey].insert(key, value)
            inserted += 1

        return IntegerType(inserted)

    def zrem(self, zkey, value):
        if zkey not in self.namespace:
            return IntegerType(0)

        self.namespace[zkey].remove(value)
        return IntegerType(1)

    def zcard(self, zkey):
        if zkey not in self.namespace:
            return IntegerType(0)
        return IntegerType(self.namespace[zkey].cardinality)

    def zcount(self, zkey, min_value, max_value):
        try:
            max_value = int(max_value)
            min_value = int(min_value)
        except (ValueError, TypeError):
            return ErrorType("value is not an integer or out of range")

        if zkey not in self.namespace:
            return IntegerType(0)

        return IntegerType(self.namespace[zkey].count(min_value, max_value))

    def zrank(self, zkey, value):
        if zkey not in self.namespace:
            return IntegerType(0)

        rank = self.namespace[zkey].rank(value)
        if rank is None:
            return StrType(None)
        return IntegerType(rank)

    def zrange(self, zkey, min_value, max_value, with_scores=None):
        # CURRENTLY INCOMPLETE
        try:
            max_value = int(max_value)
            min_value = int(min_value)
        except (ValueError, TypeError):
            return ErrorType("value is not an integer or out of range")

        if zkey not in self.namespace:
            return StrType(None)

        vals = self.namespace[zkey].range(min_value, max_value, with_scores)
        return ListType(vals)
