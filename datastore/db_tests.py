import datastore.db_packages as pk
import datastore.db_source as code

database = code.SqlalchemyDatabase("sqlite:///dbfile.db")
session = database.Session()



first_generation = pk.Package('First Generation')

base_bulbasaur = pk.Description('Bulbasaur', 'Grass Pokemon', '/wiki/Bulbasaur_(Pokémon)', 'First Generation')
bulbasaur = pk.Version('Bulbasaur', 'Bulbasaur')
ivysaur = pk.Version('Ivysaur', 'Bulbasaur')
venusaur = pk.Version('Venusaur', 'Bulbasaur')

base_charmander = pk.Description('Charmander', 'Fire Pokemon', '/wiki/Charmander_(Pokémon)', 'First Generation')
charmander = pk.Version('Charmander', 'Charmander')
charmeleon = pk.Version('Charmeleon', 'Charmander')
charizard = pk.Version('Charizard', 'Charmander')

base_squirtle = pk.Description('Squirtle', 'Water Pokemon', '/wiki/Squirtle_(Pokémon)', 'First Generation')
squirtle = pk.Version('Squirtle', 'Squirtle')
wartortle = pk.Version('Wartortle', 'Squirtle')
blastoise = pk.Version('Blastoise', 'Squirtle')


second_generation = pk.Package('Second Generation')

base_chikorita = pk.Description('Chikorita', 'Grass Pokemon', '/wiki/Chikorita_(Pokémon)', 'Second Generation')
chikorita = pk.Version('Chikorita', 'Chikorita')
bayleef = pk.Version('Bayleef', 'Chikorita')
meganium = pk.Version('Meganium', 'Chikorita')

base_cynduaquil = pk.Description('Cyndaquil', 'Fire Pokemon', '/wiki/Cyndaquil_(Pokémon)', 'Second Generation')
cynduaquil = pk.Version('Cyndaquil', 'Cyndaquil')
quilava = pk.Version('Quilava', 'Cyndaquil')
typhlosion = pk.Version('Typhlosion', 'Cyndaquil')

base_totodile = pk.Description('Totodile', 'Water Pokemon', '/wiki/Totodile_(Pokémon)', 'Second Generation')
totodile = pk.Version('Totodile', 'Totodile')
crononaw = pk.Version('Crononaw', 'Totodile')
feraligatr = pk.Version('Feraligatr', 'Totodile')

generations = [first_generation, second_generation]
pokemons = [base_bulbasaur, base_charmander, base_squirtle, base_chikorita, base_cynduaquil, base_totodile]
evolutions = [bulbasaur, ivysaur, venusaur, charmander, charmeleon, charizard, squirtle, wartortle, blastoise,
              chikorita, bayleef, meganium, cynduaquil, quilava, typhlosion, totodile, crononaw, feraligatr]

database.store(*generations)
database.store(*pokemons)
database.store(*evolutions)
database.store(bulbasaur)
database.store('ananas')

print(database.restore_from_table('First Generation', 'Ecosystem'))
print(database.restore_from_table('Asas', 'Ecosystem'))
print(database.restore_from_table('First Generation', 'Asas'))

print()

for i in database.restore_from_master('Second Generation', 'Ecosystem'):
    print(i)

print(database.restore_from_master('Asas', 'Ecosystem'))
print(database.restore_from_master('First Generation', 'Asas'))