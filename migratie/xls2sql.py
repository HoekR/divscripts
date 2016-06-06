# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 17:27:46 2016

@author: rik
"""
from normalizer import Norm, seq_nr


z = seq_nr()

class SQLTemplater(object):
    def __init__(self):
        self.n = Norm(fn = 'NT00335/NT00335_persoon.csv')
        self.rik_uuid = "2ef20ba9-df79-49cb-be97-49f949e19514"
        self.vessel_template = """
        INSERT INTO `nl_aus_migration_db_jde`.`itemtype_vessel`
        (`ID`,
         `vessel_name`,
        `vessel_UUID`,
        `vessel_type`,
        `recordCreator_UUID`,
        `recordCreated`)
        VALUES
        {values};
        """
        self.vessel_values = """\
        ({ID},"{vessel_name}","{vessel_UUID}","{vessel_type}","{recordCreator_UUID}",{recordCreated})"""
        
        self.person_template = """
        INSERT INTO `nl_aus_migration_db_jde`.`itemtype_person`
        (`ID`,
        `person_UUID`,
        `person_familyName`,
        `person_nameInitials`,
        `person_nameInterpositions`,
        `person_birth_date`,
        `recordCreator_UUID`,
        `recordCreated`,
        `NA_ID`)
        VALUES
        {values};
        """
        
        self.person_values = """({ID},"{person_UUID}","{person_familyName}","{person_nameInitials}","{person_nameInterpositions}","{person_birth_date}","{recordCreator_UUID}",\
{recordCreated},"{NA_ID}")"""        
        
        self.reis_template="""
        INSERT INTO `nl_aus_migration_db_jde`.`itemtype_event`
        (`ID`,
        `event_UUID`,
        `event_type`,
        `event_dateStart`,
        `event_dateEnd`,
        `recordCreator_UUID`,
        `recordCreated`)
        VALUES
        {values};
        """
        
        self.reis_values = """({ID},"{event_UUID}","{event_type}","{event_dateStart}","{event_dateEnd}","{recordCreator_UUID}",{recordCreated})"""
        
        self.rel_event_vessel_template = """
        INSERT INTO `nl_aus_migration_db_jde`.`rel_event_vessel` 
        (`event_UUID`,
        `vessel_UUID`,
        `recordCreator_UUID`,
        `recordCreated`)
        VALUES
        {values};
        """
        self.rev_values = """("{event_UUID}","{vessel_UUID}","{recordCreator_UUID}",{recordCreated})"""
        
        
        self.template_rel_pers_event = """
        INSERT INTO `nl_aus_migration_db_jde`.`rel_person_event`
        (`ID`,
        `event_UUID`,
        `person_UUID`,
        `recordCreator_UUID`,
        `recordCreated`)
        VALUES
        {values};
        """
        
        self.rel_pers_values = """({ID},"{event_UUID}","{person_UUID}","{recordCreator_UUID}",{recordCreated})"""
 
         
        self.template_rel_card_person = """
        INSERT INTO `nl_aus_migration_db_jde`.`rel_card_person`
          (`card_UUID`,
          `person_UUID`,
          `recordCreator_UUID`,
          `recordCreated`)
          VALUES
          {values};
          """
        self.rel_card_person_values = """("{card_UUID}","{person_UUID}","{recordCreator_UUID}",{recordCreated})"""
        


    def per2sql(self):
        t = self.person_template
        v = self.person_values
        out = [v.format(ID=int(i['prs_id']),
                                   person_familyName=i['prs_achternaam'],
                                   person_nameInitials=i['prs_initialen'],
                                   person_nameInterpositions=i['prs_tussenvoegsel'],
                                   person_birth_date=i['prs_geboortedatum'],
                                   recordCreator_UUID=self.rik_uuid,
                                   recordCreated='NOW()',
                                   NA_ID=i['prs_id'],
                                   person_UUID=i['uuid']
                                   ) for i in self.n.persons]
        out = ','.join(out)
        out = t.format(values=out)
        return out
        
    def ves2sql(self):
        t = self.vessel_template
        v = self.vessel_values
        out = [v.format(ID=self.n.vessels.index(i),
                                   vessel_name=i[2],
                                   vessel_type=i[3],
                                   vessel_UUID=i[1],
                                   recordCreator_UUID=self.rik_uuid,
                                   recordCreated='NOW()',
                                   ) for i in self.n.vessels]
        out = ','.join(out)
        out = t.format(values=out)
        return out

    def evt2sql(self):
        t = self.reis_template
        v = self.reis_values
        out = [v.format(ID=int(i['reis_id']),
                                  event_UUID=i['uuid'],
                                  event_dateStart=i['vertrek'],
                                  event_dateEnd=i['aankomst'], 
                                  event_type='migration',
                                  recordCreator_UUID=self.rik_uuid,
                                  recordCreated='NOW()',
                                  ) for i in self.n.vervoer]
        out = ','.join(out)
        out = t.format(values=out)
        return out

    def rpe2sql(self):
        t = self.template_rel_pers_event
        v = self.rel_pers_values
        out = [v.format(ID=z.next(),
                        event_UUID=i[0],
                        person_UUID=i[1],
                        recordCreator_UUID=self.rik_uuid,
                        recordCreated='NOW()',
                        ) for i in self.n.pers_reis]
        out = ','.join(out)
        out = t.format(values=out)
        return out


    def cp2sql(self):
        t = self.template_rel_card_person
        v = self.rel_card_person_values
        out = [v.format(card_UUID=i['prs_uuid'],
                        person_UUID=i['prs_id'],
                        recordCreator_UUID=self.rik_uuid,
                        recordCreated='NOW()',
                        ) for i in self.n.kaarten]
        out = ','.join(out)
        out = t.format(values=out)
        return out


    def vr2sql(self):
        t = self.rel_event_vessel_template
        v = self.rev_values
        out = [v.format(event_UUID=i[0],
                        vessel_UUID=i[1],
                        recordCreator_UUID=self.rik_uuid,
                        recordCreated='NOW()',
                        ) for i in self.n.v_reis]
        out = ','.join(out)
        out = t.format(values=out)
        return out        

        
    def templater(self, basedir):
        
        p_out = open('new_db/sql_pers_gen.sql', 'w')
        for m in (self.per2sql, 
                  self.ves2sql, 
                  self.evt2sql, 
                  self.rpe2sql,
                  self.cp2sql,
                  self.vr2sql):
            out = m()
            p_out.write(out)
            p_out.write('\n\n')        
        p_out.close()
        print "{fl} written".format(fl=p_out.name)
        