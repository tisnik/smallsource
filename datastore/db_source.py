import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import datastore.db_packages as pk

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
        # TODO: check if item exists first
        session = self.Session()
        for package in args:
            package_to_dict = package.to_dict()

            # TODO: excepts for bad args
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

# TODO: add excepts for bad args
    def restore_from_table(self, arg, table):
        session = self.Session()
        if table.title() == 'Ecosystem':
            eco = session.query(Ecosystem).filter_by(jmeno=arg).first()
            package = pk.Package(eco.jmeno)
        elif table.title() == 'Packages':
            pack = session.query(Packages).filter_by(name=arg).first()
            package = pk.Description(pack.name, pack.description, pack.repo, pack.eco)
        elif table.title() == 'Versions':
            ver = session.query(Versions).filter_by(version=arg).first()
            package = pk.Version(ver.version, ver.package)
        return package

    def restore_from_master(self, arg, table):
        session = self.Session()
        packages = []
        if table.title() == 'Ecosystem':
            object = session.query(Ecosystem).filter_by(jmeno=arg).first()
            id = object.id
            packs_from_db = session.query(Packages).filter_by(eco_id=id).all()
            for pack in packs_from_db:
                package = pk.Description(pack.name, pack.description, pack.repo, pack.eco)
                packages.append(package)
        elif table.title() == 'Packages':
            packObj = session.query(Packages).filter_by(name=arg).first()
            packName = packObj.name
            vers = session.query(Versions).filter_by(package=packName).all()
            for ver in vers:
                version = pk.Version(ver.version, ver.package)
                packages.append(version)
        return packages

    # TODO: search in database (arg - name and column)


database = SqlalchemyDatabase("sqlite:///dbfile.db")
session = database.Session()
