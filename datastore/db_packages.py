class Package(object):
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def __str__(self):
        return 'Name: {}'.format(self.jmeno)

    def to_dict(self):
        dictionary = dict()
        dictionary["jmeno"] = self.jmeno
        return dictionary

    @staticmethod
    def from_dict(dict):
        dictionary = dict
        result = Package(dictionary['jmeno'])
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

first_generation = Package('First Generation')

base_bulbasaur = Description('Bulbasaur', 'Grass Pokemon', '/wiki/Bulbasaur_(Pokémon)', 'First Generation')
bulbasaur = Version('Bulbasaur', 'Bulbasaur')
ivysaur = Version('Ivysaur', 'Bulbasaur')
venusaur = Version('Venusaur', 'Bulbasaur')

base_charmander = Description('Charmander', 'Fire Pokemon', '/wiki/Charmander_(Pokémon)', 'First Generation')
charmander = Version('Charmander', 'Charmander')
charmeleon = Version('Charmeleon', 'Charmander')
charizard = Version('Charizard', 'Charmander')

base_squirtle = Description('Squirtle', 'Water Pokemon', '/wiki/Squirtle_(Pokémon)', 'First Generation')
squirtle = Version('Squirtle', 'Squirtle')
wartortle = Version('Wartortle', 'Squirtle')
blastoise = Version('Blastoise', 'Squirtle')


second_generation = Package('Second Generation')

base_chikorita = Description('Chikorita', 'Grass Pokemon', '/wiki/Chikorita_(Pokémon)', 'Second Generation')
chikorita = Version('Chikorita', 'Chikorita')
bayleef = Version('Bayleef', 'Chikorita')
meganium = Version('Meganium', 'Chikorita')

base_cynduaquil = Description('Cyndaquil', 'Fire Pokemon', '/Cyndaquil_(Pokémon)', 'Second Generation')
cynduaquil = Version('Cyndaquil', 'Cyndaquil')
quilava = Version('Quilava', 'Cyndaquil')
typhlosion = Version('Typhlosion', 'Cyndaquil')

base_totodile = Description('Totodile', 'Water Pokemon', '/Totodile_(Pokémon)', 'Second Generation')
totodile = Version('Totodile', 'Totodile')
crononaw = Version('Crononaw', 'Totodile')
feraligatr = Version('Feraligatr', 'Totodile')
