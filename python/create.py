#!/usr/bin/env python
# Usage create.py TABLE_NAME
# Drop (i.e. delete) any existing table with this name, create a new table and add special columns needed for cartodby.
# If the cartodbfy stage is omitted a 'ghost' table is created, i.e. absent from CartoDB web interface.

from cartodb import CartoDBAPIKey, CartoDBException
from my_keys import CARTODB_API_KEY, cartodb_domain

def create( table_name, columns, api_key=CARTODB_API_KEY, cartodb_domain=cartodb_domain):
   cl = CartoDBAPIKey(api_key, cartodb_domain)
   try:
      resp = cl.sql("drop table {}".format(table_name))
   except CartoDBException as e:
      print ("unable to drop table", e)
      
   # Do not add column 'cartodb_id' as this is created by the later call to cdb_cartodbfytable()
   # Though if it were needed, it would most likely look like this -
   # cartodb_id int4 default nextval('untitled_table_cartodb_id_seq1'::regclass) not null
   # Columns created_at, updated_at, the_geometry and the_geom_webmercator are also created automatically if absent.
   # created_at timestamptz default now() not null, updated_at timestamptz default now() not null
   # the_geometry, the_geom_webmercator geometry
   try:
      resp = cl.sql("create table {} ({})".format(table_name, columns))
   except CartoDBException as e:
      print ("unable to create table", e)

   print resp

   try:
      resp = cl.sql("select cdb_cartodbfytable('{}')".format(table_name))
   except CartoDBException as e:
      print ("unable to cartodbfy table", e)
   return

def main( table_name ):
   create( table_name, "name text, description text" )
   return

if __name__ == "__main__":
   from sys import argv
   main( argv[1] )

