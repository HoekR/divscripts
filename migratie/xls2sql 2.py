# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:27:46 2016

@author: rik
"""

import normalizer

class sqltemplater(object):
    def __init__(self):
        self.n = Norm()
        self.rik_uuid = "2ef20ba9-df79-49cb-be97-49f949e19514"
        self.vessel_template = """
        INSERT INTO `nl_aus_migration_db_jde`.`itemtype_vessel`
        (`ID`,
        `vessel_name`,
        `vessel_type`,
        `vessel_description`,
        `recordCreator_UUID`,
        `recordCreated`)
        VALUES
        ({ID},
        {vessel_name},
        {vessel_type},
        {vessel_description},
        {recordCreator_UUID},
        {recordCreated});
        """
        
        self.person_template = """
        INSERT INTO `nl_aus_migration_db_jde`.`itemtype_person`
        (`ID`,
        `person_familyName`,
        `person_nameInitials`,
        `person_nameInterpositions`,
        `person_birth_date`,
        `recordNotes`,
        `recordCreator_UUID`,
        `recordCreated`,
        `NA_ID`)
        VALUES
        ({ID},
        {person_familyName},
        {person_givenNames},
        {person_nameInitials},
        {person_nameInterpositions},
        {person_birth_date},
        {recordNotes},
        {recordCreator_UUID},
        {recordCreated},
        {NA_ID});
        """
        
        self.reis_template="""
        INSERT INTO `nl_aus_migration_db_jde`.`itemtype_event`
        (`ID`,
        `event_type`,
        `event_name`,
        `event_dateStart`,
        `event_dateEnd`,
        `recordCreator_UUID`,
        `recordCreated`)
        VALUES
        ({ID},
        {event_type},
        {event_name},
        {event_dateStart},
        {event_dateEnd},
        {recordCreator_UUID},
        {recordCreated});
        """
        
        self.template_rel_pers_event = """
        INSERT INTO `nl_aus_migration_db_jde`.`rel_person_event`
        (`ID`,
        `event_UUID`,
        `person_UUID`,
        `recordCreator_UUID`,
        `recordCreated`)
        VALUES
        ({ID},
        {event_UUID},
        {person_UUID},
        {recordCreator_UUID},
        {recordCreated});
        """        
    
    def templater(self):
        p_out = open('/home/rik/Dropbox/Link to emigrantenkaarten/new_db')
        out = [self.person_template.format(ID=int(i['prs_id']),
                                           person_familyName=i['prs_achternaam'],
                                           person_nameInitials=i['prs_initialen'],
                                           person_nameInterpositions=i['prs_tussenvoegsel'],
                                           person_birth_date=i['prs_geboortedatum'],
                                           recordNotes=i['archieflink'],
                                           recordCreator_UUID=self.rik_uuid,
                                           recordCreated='now()',
                                           NA_ID=i['prs_uuid']
                                           ) for i in self.n.persons]
        p_out.write(out)
        p_out.close()
        print "{fl} written".format(fl=p_out.name)
        