class Package(object):
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def __str__(self):
        return 'Name: {}'.format(self.jmeno)

    def to_dict(self):
        dictionary = dict()
        dictionary["name"] = self.jmeno
        return dictionary

    @staticmethod
    def from_dict(dict):
        dictionary = dict
        result = Package(dictionary['name'])
        return result


class Description(object):
    def __init__(self, name, description, repo, package):
        self.name = name
        self.description = description
        self.repo = repo
        self.package = package

    def __str__(self):
        return 'Name: {}, Description: {}, Repo: {}'.format(self.name, self.description, self.repo)


    def to_dict(self):
        dictionary = dict()
        dictionary["name"] = self.name
        dictionary["description"] = self.description
        dictionary["repo"] = self.repo
        dictionary['eco'] = self.package
        return dictionary

    @staticmethod
    def from_dict(dict):
        result = Description(dict['name'], dict['description'], dict['repo'], dict['eco'])
        return result


class Version(object):
    def __init__(self, version, package):
        self.version = version
        self.package = package

    def __str__(self):
        return 'Version: {}'.format(self.version)

    def to_dict(self):
        dictionary = dict()
        dictionary["version"] = self.version
        dictionary['pack'] = self.package
        return dictionary

    @staticmethod
    def from_dict(dict):
        result = Version(dict['version'], dict['package'])
        return result
