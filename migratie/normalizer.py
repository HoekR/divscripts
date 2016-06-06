# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 11:47:25 2016

@author: rik
"""
import os
import csv
from uuid import uuid1

#from random import choice
#from collections import Counter

def seq_nr():
    x = 1
    while True:    
        yield x
        x += 1

z = seq_nr()


class Norm(object):
    def __init__(self, fn=''):    
        self.persons = []
        self.vessel = []
        self.vessels = []
        self.vervoer = []
        self.pers_reis = []
        self.v_reis = []
        self.kaarten = []
        if fn:
            self.fn = fn
        else:
            self.fn = '/home/rik/Dropbox/Link to emigrantenkaarten/NT00335/NT00335_persoon.csv'
#        self.vessel_reis = []
        self.make_data()
    
    def make_data(self):
        with open(self.fn) as f:
            reader = csv.DictReader(f)
            for row in reader:
                person   = {k: row[k] for k in ['prs_id',
                               'prs_achternaam',
                               'prs_tussenvoegsel',
                               'prs_initialen',
                               'prs_geboortedatum']}
                person['uuid'] = uuid1()
                voertuig = [row[k] for k in ['naam_vervoer','type_vervoer']]
                kaartje = {k:row[k] for k in ['prs_id', 
                                              'prs_uuid',
                                              'kaartenbak',
                                              'archieflink']}
                if voertuig not in self.vessel:
                    self.vessel.append(voertuig)
                    v_id = self.vessel.index(voertuig)
                    v = [v_id, str(uuid1()), voertuig[0], voertuig[1]]
                    self.vessels.append(v)
                reis = {k: row[k] for k in 
                        ['vertrek',
                        'aankomst']}
                reis['reis_id'] = z.next()
                reis['uuid'] = '%s' % uuid1()
                reis['vessel_id'] = v[1]
                self.v_reis.append([v[0], reis['reis_id']])
                self.pers_reis.append([person['prs_id'], reis['reis_id']])
                self.vervoer.append(reis)
                self.persons.append(person)
                self.kaarten.append(kaartje)
                self.reis = reis
                self.person = person
        
    def writeout(self, basedir=''):
        """need to clean this up"""
        
                
        flout3 = open(os.path.join(basedir, 'new_db/voertuig.csv'), 'w')
        w = csv.writer(flout3)
        w.writerow(['id', 'naam', 'type','RecordCreatorUUID'])
        w.writerows(self.vessels)
        flout3.close()
        
        flout2 = open(os.path.join(basedir, 'new_db/reis.csv'), 'w')
        w = csv.DictWriter(flout2, self.reis.keys())
        w.writeheader()
        w.writerows(self.vervoer)
        flout2.close()
        
        
        flout = open(os.path.join(basedir, 'new_db/pers.csv'), 'w')
        w = csv.DictWriter(flout, self.person.keys())
        w.writeheader()
        w.writerows(self.persons)
        flout.close()
        
        flout4 = open(os.path.join(basedir, 'new_db/pers_reis.csv'), 'w')
        w = csv.writer(flout4)
        w.writerow(['prs_id', 'reis_id'])
        w.writerows(self.pers_reis)
        flout.close()
        
        flout5 = open(os.path.join(basedir, 'new_db/kaarten.csv'), 'w')
        w = csv.DictWriter(flout5, ['prs_id', 'prs_uuid','kaartenbak','archieflink'])
        w.writerows(self.kaarten)
        flout.close()
        
        
#    def writesql(self):
#       