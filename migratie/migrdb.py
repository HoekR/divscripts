# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, Numeric, String, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DigitalObjectAnnotation(Base):
    __tablename__ = 'digital_object_annotations'

    ID = Column(Integer, primary_key=True)
    rel_UUID = Column(String(250))
    doc_UUID = Column(String(250))
    doc_descriptionAbstract = Column(Integer)
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class DigitalObjectCatalogue(Base):
    __tablename__ = 'digital_object_catalogue'

    ID = Column(Integer, primary_key=True)
    doc_UUID = Column(String(250))
    doc_title = Column(String(255))
    doc_titleAlternative = Column(String(250))
    doc_fileFormat = Column(String(250))
    doc_formatSizeOrDuration = Column(String(250))
    doc_mimeType = Column(String(250))
    doc_spatial = Column(String(250))
    doc_subject = Column(String(250))
    doc_language = Column(String(250))
    doc_coverage = Column(String(250))
    doc_accessRights = Column(String(250))
    doc_rightsHolder = Column(String(250))
    doc_fileName = Column(String(250))
    doc_fileLocation = Column(String(255))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class ItemtypeEvent(Base):
    __tablename__ = 'itemtype_event'

    ID = Column(Integer, primary_key=True)
    event_UUID = Column(String(250))
    event_dataTableName = Column(String(250))
    event_dataTableNameUUID = Column(String(250))
    event_type = Column(String(250))
    event_name = Column(String(250))
    event_shortName = Column(String(250))
    event_alternativeName = Column(String(250))
    event_dateCoverage = Column(String(250))
    event_dateStart = Column(String(250))
    event_dateEnd = Column(String(250))
    event_place = Column(String(250))
    event_summary = Column(String)
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class ItemtypeInstitution(Base):
    __tablename__ = 'itemtype_institution'

    ID = Column(Integer, primary_key=True)
    institution_UUID = Column(String(250))
    institution_name = Column(String(250))
    institution_type = Column(String(250))
    institution_place = Column(String(250))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class ItemtypePerson(Base):
    __tablename__ = 'itemtype_person'

    ID = Column(Integer, primary_key=True)
    person_UUID = Column(String(250))
    person_familyName = Column(String(255))
    person_givenNames = Column(String(250))
    person_nameInitials = Column(String(250))
    person_nameInterpositions = Column(String(250))
    person_alternateName = Column(String(250))
    person_summary = Column(String)
    person_role = Column(String(250))
    person_birth_date = Column(String(250))
    person_birth_place = Column(String(250))
    person_death_date = Column(String(250))
    person_death_place = Column(String(250))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))
    NA_ID = Column(String(45))


class ItemtypeRelation(Base):
    __tablename__ = 'itemtype_relation'

    ID = Column(Integer, primary_key=True)
    rel_UUID = Column(String(250))
    rel_relationType = Column(String(250))
    rel_relationDescription = Column(String)
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class ItemtypeUnit(Base):
    __tablename__ = 'itemtype_unit'

    ID = Column(Integer, primary_key=True)
    unit_UUID = Column(String(250))
    unit_name = Column(String(250))
    unit_description = Column(String)
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class ItemtypeVessel(Base):
    __tablename__ = 'itemtype_vessel'

    ID = Column(Integer, primary_key=True)
    vessel_UUID = Column(String(250))
    vessel_callsign = Column(String(250))
    vessel_name = Column(String(250))
    vessel_type = Column(String(250))
    vessel_description = Column(String(255))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250), nullable=False)
    recordCreated = Column(String(250), nullable=False)


class RelDigitalObjectsInstitution(Base):
    __tablename__ = 'rel_digital_objects_institution'

    ID = Column(Integer, primary_key=True)
    rel_UUID = Column(String(250))
    doc_UUID = Column(String(250))
    institution_UUID = Column(String(250))
    rel_bibliographicCitation = Column(String(250), index=True)
    rel_bibliographicResource = Column(String(250))
    rel_bibliographicUrl = Column(String(250))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class RelDigitalObjectsPerson(Base):
    __tablename__ = 'rel_digital_objects_person'

    ID = Column(Integer, primary_key=True)
    rel_UUID = Column(String(250))
    doc_UUID = Column(String(250))
    person_UUID = Column(String(250))
    rel_relationType = Column(String(250))
    rel_relationDescription = Column(String(250))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class RelPersonEvent(Base):
    __tablename__ = 'rel_person_event'

    ID = Column(Integer, primary_key=True)
    rel_UUID = Column(String(250))
    event_UUID = Column(String(250))
    person_UUID = Column(String(250))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class RelPersonInstitution(Base):
    __tablename__ = 'rel_person_institution'

    ID = Column(Integer, primary_key=True)
    rel_UUID = Column(String(250))
    institution_UUID = Column(String(250))
    person_UUID = Column(String(250))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class RelPersonUnit(Base):
    __tablename__ = 'rel_person_unit'

    ID = Column(Integer, primary_key=True)
    rel_UUID = Column(String(250))
    unit_UUID = Column(String(250))
    person_UUID = Column(String(250))
    recordRemarks = Column(String)
    recordNotes = Column(String)
    recordCreator_UUID = Column(String(250))
    recordCreated = Column(String(250))


class RepositoryLocation(Base):
    __tablename__ = 'repository_location'

    id = Column(Integer, primary_key=True)
    country = Column(String(25), nullable=False)
    city = Column(String(40), nullable=False)
    latitude = Column(Float(10, True), nullable=False)
    longitude = Column(Float(10), nullable=False)
    altitude = Column(Float(5), nullable=False)
    country_code = Column(String(2), nullable=False)
    continent_code = Column(String(2), nullable=False)
    continent = Column(String(25), nullable=False)


class RepositoryLocationContinent(Base):
    __tablename__ = 'repository_location_continent'

    ID = Column(Integer, primary_key=True)
    continent = Column(Text, nullable=False)
    country = Column(Text, nullable=False)


class RepositoryLocationContinentName(Base):
    __tablename__ = 'repository_location_continent_name'

    ID = Column(Integer, primary_key=True)
    code = Column(Text, nullable=False)
    name = Column(Text, nullable=False)


class RepositoryLocationCountry(Base):
    __tablename__ = 'repository_location_country'

    ID = Column(Integer, primary_key=True)
    Country = Column(String(44))
    Alpha2_Code = Column(String(2))
    Alpha3_Code = Column(String(3))
    Numeric_Code = Column(Integer)
    Latitude = Column(Numeric(7, 4))
    Longitude = Column(Numeric(8, 4))


class RepositoryRecordCreator(Base):
    __tablename__ = 'repository_record_creator'

    ID = Column(Integer, primary_key=True)
    recordCreator_UUID = Column(String(250))
    recordCreator_fullName = Column(String(255))
    recordCreator_dateCreated = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    recordCreator_description = Column(Text)
    recordCreator_type = Column(String(255))
    recordCreator_email = Column(String(255))
    recordCreator_dateExpire = Column(String(255))
    recordCreator_userName = Column(String(255))
    recordCreator_passWord = Column(String(255))
