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
        session = self.Session()
        package_in_db = None
        for package in args:

            try:
                package_to_dict = package.to_dict()
                if 'eco' in package_to_dict:
                    exists = self.restore_from_table(package_to_dict['name'], 'packages')
                    if exists is None:
                        eco = session.query(Ecosystem).filter_by(jmeno=package_to_dict['eco']).first()
                        package_to_dict['eco'] = eco
                        package_in_db = Packages(** package_to_dict)
                        print(package_to_dict)
                elif 'pack' in package_to_dict:
                    exists = self.restore_from_table(package_to_dict['version'], 'versions')
                    if exists is None:
                        pack = session.query(Packages).filter_by(name=package_to_dict['pack']).first()
                        package_to_dict['pack'] = pack
                        package_in_db = Versions(** package_to_dict)
                elif 'jmeno' in package_to_dict:
                    exists = self.restore_from_table(package_to_dict['jmeno'], 'ecosystem')
                    if exists is None:
                        package_in_db = Ecosystem(** package_to_dict)
                else:
                    print('Bad Arguments')
                if package_in_db is not None:
                    session.add(package_in_db)
            except Exception as e:
                print(e)
        session.commit()

    def restore_from_table(self, name, table):

        session = self.Session()
        try:
            if table.title() == 'Ecosystem':
                eco = session.query(Ecosystem).filter_by(jmeno=name).first()
                if eco is None:
                    return None
                package = pk.Package(eco.jmeno)
            elif table.title() == 'Packages':
                pack = session.query(Packages).filter_by(name=name).first()
                if pack is None:
                    return None
                package = pk.Description(pack.name, pack.description, pack.repo, pack.eco)
            elif table.title() == 'Versions':
                ver = session.query(Versions).filter_by(version=name).first()
                if ver is None:
                    return None
                package = pk.Version(ver.version, ver.package)
            else:
                print('Badly defined table to add to')
            return package
        except Exception as e:
            print(e)

    def restore_from_master(self, name, master_table):
        session = self.Session()
        packages = []

        try:
            if master_table.title() == 'Ecosystem':
                package = session.query(Ecosystem).filter_by(jmeno=name).first()
                if package is None:
                    return None
                id = package.id
                packs_from_db = session.query(Packages).filter_by(eco_id=id).all()
                for pack in packs_from_db:
                    package = pk.Description(pack.name, pack.description, pack.repo, pack.eco)
                    packages.append(package)
            elif master_table.title() == 'Packages':
                package = session.query(Packages).filter_by(name=name).first()
                if package is None:
                    return None
                name = package.name
                vers = session.query(Versions).filter_by(package=name).all()
                for ver in vers:
                    version = pk.Version(ver.version, ver.package)
                    packages.append(version)
            else:
                print('Bad master table')
            return packages
        except Exception as e:
            print(e)
