class ReturnType:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class ErrorType(ReturnType):

    def __repr__(self):
        return "(error) ERR {}".format(self.value)


class IntegerType(ReturnType):

    def __repr__(self):
        return "(integer) {}".format(self.value)


class ListType(ReturnType):

    def __repr__(self):
        return '\n'.join([') "{}"'.format(x) for x in self.value])


class StrType(ReturnType):

    def __repr__(self):
        if self.value is None:
            v = "(nil)"
        else:
            v = self.value
        return '"{}"'.format(v)
