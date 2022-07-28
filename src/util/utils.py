import jsonpickle


class Replacement:
    def __init__(self, original, new, reason=None):
        super().__init__()
        self.original = original
        self.new = new
        self.reason = reason


class Upgrade(list):
    VERSION = 1

    def __init__(self):
        super().__init__()
        self.version = Upgrade.VERSION

    def save(self, path):
        with open(path + '.ugr', 'w', encoding='utf8') as output:
            output.write(jsonpickle.encode(self))

    @staticmethod
    def load(path):
        with open(path, 'r', encoding='utf8') as inpath:
            content = inpath.read()
            data = jsonpickle.decode(content)
            if data.version == Upgrade.VERSION:
                return data
            else:
                raise TypeError("invalid upgrade file version")

    def add_if_not_present(self, replacement):
        if (replacement.original, replacement.new) not in [(r.original, r.new) for r in self]:
            self.append(replacement)


class Similar:
    def __init__(self, dropped, saved, property, degree):
        self.saved = saved
        self.dropped = dropped
        self.property = property
        self.degree = degree

    def human_readable(self):
        return "'{}' (dropped) is {:.2%} similar to '{}' (saved)".format(
            self.dropped[self.property],
            self.degree,
            self.saved[self.property])


class Regenerated:
    def __init__(self, pattern, original, new):
        self.pattern = pattern
        self.original = original
        self.new = new

    def human_readable(self):
        return '"{}" id is regenerated to "{}" based on "{}"'.format(
            self.original['ID'],
            self.new['ID'],
            self.pattern)