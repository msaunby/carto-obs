#!/usr/bin/env python
# Usage drop.py TABLE_NAME
# Drop (i.e. delete) any existing table with this name.

from cartodb import CartoDBAPIKey, CartoDBException
from my_keys import CARTODB_API_KEY, cartodb_domain

def drop( table_name, api_key=CARTODB_API_KEY, cartodb_domain=cartodb_domain):
   cl = CartoDBAPIKey(api_key, cartodb_domain)
   try:
      resp = cl.sql("drop table {}".format(table_name))
   except CartoDBException as e:
      print ("unable to drop table", e)
      
def main( table_name ):
   drop( table_name )
   return

if __name__ == "__main__":
   from sys import argv
   main( argv[1] )

