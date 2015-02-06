#!/usr/bin/env python
from cartodb import CartoDBAPIKey, CartoDBException
from my_keys import CARTODB_API_KEY, cartodb_domain


def describe( table_name ):
   cl = CartoDBAPIKey(CARTODB_API_KEY, cartodb_domain)
   try:
      resp = cl.sql("SELECT * FROM information_schema.columns WHERE table_name ='{}'".format(table_name))
   except CartoDBException as e:
      print ("some error ocurred", e)

   #print resp.keys()
   #for c in resp['fields']:
   #   print c, resp['fields'][c]

   for c in resp['rows']:
      #print "-----------"
      #for d in ['column_name','udt_name','column_default']:
      #for d in c:
      #   if c[d] != None:
      #      print d, c[d]
      item = "{} {}".format(c['column_name'], c['udt_name'])
      if c['column_default']:
         item = item + " default " + c['column_default']
      print item


def main( table_name ):
   describe( table_name )
   return

if __name__ == "__main__":
   from sys import argv
   main( argv[1] )
