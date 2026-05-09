_current = None


def login(employee):
    global _current
    _current = employee


def logout():
    global _current
    _current = None


def get():
    return _current
