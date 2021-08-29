class RegisterDecorator(object):
    def __init__(self):
        self._registered = []

    def __getitem__(self, item):
        return self._registered[item]

    def register(self):
        def wrapper(func):
            self._registered.append(func)
            return f
        return wrapper