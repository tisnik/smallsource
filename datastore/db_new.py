import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import datastore.packageclass as pk

metadata = sqla.MetaData()
Base = declarative_base()


class Ecosystem(Base):
    __tablename__ = 'ecosystem'
    id = sqla.Column(sqla.Integer, primary_key=True)
    jmeno = sqla.Column(sqla.String)
    packages = relationship('Packages', backref='eco')


class Packages(Base):
    __tablename__ = 'packages'
    id = sqla.Column(sqla.Integer, primary_key=True)
    eco_id = sqla.Column(sqla.Integer, sqla.ForeignKey('ecosystem.id'))
    name = sqla.Column(sqla.String)
    description = sqla.Column(sqla.String)
    repo = sqla.Column(sqla.String)
    versions = relationship('Versions', backref='pack')


class Versions(Base):
    __tablename__ = 'versions'
    id = sqla.Column(sqla.Integer, primary_key=True)
    version = sqla.Column(sqla.String)
    package = sqla.Column(sqla.String, sqla.ForeignKey('packages.name'))



class SqlalchemyDatabase(object):
    def __init__(self, backend):
        engine = sqla.create_engine(backend, echo=False)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        session = self.Session()

    def store(self, *args):
        session = self.Session()
        for package in args:
            package_to_dict = package.to_dict()

            if 'eco' in package_to_dict:
                eco = session.query(Ecosystem).filter_by(jmeno=package_to_dict['eco']).first()
                package_to_dict['eco'] = eco
                package_in_db = Packages(** package_to_dict)
            elif 'pack' in package_to_dict:
                pack = session.query(Packages).filter_by(name=package_to_dict['pack']).first()
                package_to_dict['pack'] = pack
                package_in_db = Versions(** package_to_dict)
            else:
                package_in_db = Ecosystem(** package_to_dict)

            session.add(package_in_db)
        session.commit()

database = SqlalchemyDatabase("sqlite:///dbfile.db")

database.store(
    *[pk.first_generation, pk.second_generation,
    pk.base_bulbasaur, pk.base_charmander, pk.base_squirtle,
    pk.bulbasaur, pk.ivysaur, pk.venusaur,
    pk.charizard, pk.charmander, pk.charmeleon,
    pk.squirtle, pk.wartortle, pk.blastoise,
    pk.base_chikorita, pk.base_cynduaquil, pk.base_totodile,
    pk.chikorita, pk.bayleef, pk.meganium,
    pk.cynduaquil, pk.quilava, pk.typhlosion,
    pk.totodile, pk.crononaw, pk.feraligatr]
)