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

    def restore_eco(self, jmeno):
        eco_from_db = session.query(Ecosystem).filter_by(jmeno=jmeno).first()
        package = pk.Package(eco_from_db.jmeno)
        return package

    def restore_pack(self, name):
        pack_from_db = session.query(Packages).filter_by(name=name).first()
        pack = pk.Description(pack_from_db.name, pack_from_db.description, pack_from_db.repo, pack_from_db.eco)
        return pack

    def restore_pack_with_eco(self, eco):
        ecoObj = session.query(Ecosystem).filter_by(jmeno=eco).first()
        ecoId = ecoObj.id
        packs_from_db = session.query(Packages).filter_by(eco_id=ecoId).all()
        packs = []
        for pack_from_db in packs_from_db:
            pack = pk.Description(pack_from_db.name, pack_from_db.description, pack_from_db.repo, pack_from_db.eco)
            packs.append(pack)
        return packs

    def restore_ver(self, version):
        ver_from_db = session.query(Versions).filter_by(version=version).first()
        ver = pk.Version(ver_from_db.version, ver_from_db.package)
        return ver

    def restore_ver_with_pack(self, pack):
        packObj = session.query(Packages).filter_by(name=pack).first()
        packName = packObj.name
        vers_from_db = session.query(Versions).filter_by(package=packName).all()
        vers = []
        for ver_from_db in vers_from_db:
            ver = pk.Version(ver_from_db.version, ver_from_db.package)
            vers.append(ver)
        return vers

database = SqlalchemyDatabase("sqlite:///dbfile.db")
session = database.Session()
print(database.restore_eco('First Generation'))
for i in database.restore_pack_with_eco('First Generation'):
    print(i)
for i in database.restore_ver_with_pack('Bulbasaur'):
    print(i)
