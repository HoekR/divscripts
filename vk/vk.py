"""import sqlalchemy, oursql
from sqlalchemy import MetaData
db = sqlalchemy.create_engine('mysql+oursql://root:Xochi@localhost/vk')

#create table objects
meta=MetaData()
meta.reflect(bind=db)

#print tables
for table in meta.sorted_tables:
 	print table

from sqlalchemy.sql import select
s = select([persoon])
db.execute(s)
result = db.execute(s)

persoon = meta.tables['persoon']

from sqlalchemy.sql import func

>>> s2 = select([funnaam.c.naam, func.count(functies.c.persoon)], from_obj=[ functies.join(funnaam, funnaam.c.naam)]).group_by(funnaam.c.naam)
>>> print s2
SELECT functienaam.naam, count(functie.persoon) AS count_1 
FROM functie JOIN functienaam ON functienaam.naam GROUP BY functienaam.naam
>>> res2 = db.execute(s2)
>>> res2.first()"""

#gejat van Jelle :-)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy import Float, UnicodeText, Text, Binary
#from sqlalchemy.orm import relation
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relation, backref

#from sqlalchemy.databases.mysql import MSString
from sqlalchemy.types import TIMESTAMP
# MySQL specific type to raise size limit from 16K to 16M
#from sqlalchemy.databases.mysql import MSMediumText

import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
#from sqlalchemy import MetaData
#a_db = sqlalchemy.create_engine('mysql://localhost/vk')
a_db = sqlalchemy.create_engine('mysql+oursql://root:Xochi@localhost/vk')
#meta=MetaData()
Base = declarative_base()
ENCODING = 'utf8'



class Persoon(Base):
    __tablename__ = 'persoon'

    sorteernaam = Column(u'sorteernaam', Unicode(100))
    preposities = Column(u'preposities', Unicode(50))
    voornamen = Column(u'voornamen', Unicode(255))
    geslachtsnaam = Column(u'geslachtsnaam', Unicode(255))
    intraposities = Column(u'intraposities', Unicode(50))
    postposities = Column(u'postposities', Unicode(50))
    naamstype = Column(u'naamstype', Unicode(255))
    karakteristiek = Column(u'karakteristiek', Text())
    gebjaar = Column(u'gebjaar', Integer())
    sterfjaar = Column(u'sterfjaar', Integer())
    p_id = Column(u'p_id', Integer(), primary_key=True)

    

class Functienaam(Base):
    __tablename__ = 'functienaam'

    ID_functienaam = Column(u'ID_functienaam', Integer(11), primary_key=True)
    naam = Column(u'naam', Unicode(255))

 
class Functies(Base):
    __tablename__ = 'functie'

    functienaam = Column(
                         Integer(11),
                         ForeignKey(Functienaam.ID_functienaam),
                         primary_key=True,
                         )
    beginDag = Column(u'beginDag', Integer(11))
    beginMaand = Column(u'beginMaand', Integer(11))
    beginJaar = Column(u'beginJaar', Integer(11))
    eindDag = Column(u'eindDag', Integer(11))
    eindMaand = Column(u'eindMaand', Integer(11))
    eindJaar = Column(u'eindJaar', Integer(11))
    persoon = Column(u'persoon', Integer(11))
    instelling = Column(u'instelling', Integer(11))
#    id = Column(u'id', Integer(20), primary_key=True)

    naam = relation(Functienaam)
    # ,                       primaryjoin = functienaam == Functienaam.ID_functienaam)
    #person = relation

   
class DB(object):
    def __init__(self, engine, encoding=ENCODING):
        self.engine = engine
       
        self.metadata = Base.metadata
        self.metadata.bind = engine
        self.user = ''
       
        Session = sessionmaker(bind=engine)

db = DB(a_db, encoding='utf-8')


"""usage

>>> Session = sessionmaker(bind=vk.db)
>>> session = Session()
>>> session.query(vk.Persoon).order_by(vk.Persoon.gebjaar)
"""

