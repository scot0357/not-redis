class NamespaceManager:

    def __init__(self):
        self.namespaces = {}

    def get_namespace(self, name):
        if name not in self.namespaces:
            self.namespaces[name] = {}
        return self.namespaces[name]

    def clear_namespace(self, name):
        if name in self.namespaces:
            self.namespaces[name] = {}
