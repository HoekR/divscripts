# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 11:40:03 2016

@author: rikhoekstra
"""
from sqlalchemy import create_engine
create_engine("mysql+pymysql://root:X0chiMysql@localhost/nl_aus_migration_db_jde_copy")
conn = engine.connect()
conn.