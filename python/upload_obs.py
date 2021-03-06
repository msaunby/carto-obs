#!/usr/bin/env python
from cartodb import CartoDBAPIKey, CartoDBException
import requests
from my_keys import CARTODB_API_KEY, cartodb_domain, DATAPOINT_API_KEY

cl = CartoDBAPIKey(CARTODB_API_KEY, cartodb_domain)
srid = 4326 # Spatial ref ID EPSG:4326

DATAPOINT_URL = 'http://datapoint.metoffice.gov.uk' 
datapoint_obs_path = 'public/data/val/wxobs/all/json/all'

col_names = {
   'W': 'weather_type',
   'V': 'visibility',
   'T': 'temperature',
   'S': 'wind_speed',
   'P': 'pressure',
   'G': 'wind_gust',
   'D': 'wind_direction',
   'Pt': 'pressure_tendency',
   'Dp': 'dew_point',
   'H': 'screen_relative_humidity'}

def fetchObs(api_key=DATAPOINT_API_KEY):
   params = dict()
   payload = {'key': api_key, 'res': 'hourly'}
   payload.update(params)
   url = "%s/%s" % (DATAPOINT_URL, datapoint_obs_path)
   req = requests.get(url, params=payload)
   try:
      data = req.json()
   except ValueError:
      raise Exception("DataPoint has not returned any data, this could be due to an incorrect API key")
   #print data['SiteRep']['DV']['Location'][0].keys()
   #qq = data['SiteRep']['DV']['Location'][0]['Period']   
   #for q in qq:
   #   print q.keys()
   #   print q['type']
   #   print q['value']
   #   rr = q['Rep']
   #   date =  q['value'][0:10]
   #   for r in rr:
   #      print '** keys', r.keys()
   #      print "** r['$']", r['$']
   #      hour = int(r['$'])/60
   #      print "{date} {HH:02d}:00+00:00".format(date=date,HH=hour)
   return data

def upload(table_name, data=fetchObs()):
   empty_row = dict()

   for k in col_names.keys():
      empty_row[k] = "null"

   # Delete all rows from table
   try:
      resp = cl.sql("truncate table {}".format(table_name))
   except CartoDBException as e:
      print ("some error ocurred", e)

   # The nesting of for loops here reflects the way the returned datapoint data is structured.
   # For each location there's two 'day' periods, i.e. today and yesterday. Within each of
   # these there's a set of observations for each hour.
   # The latest hour often doesn't have a full set of observations, the previous hour typically does.
   # Though not all stations report all parameter.
   for rec in data['SiteRep']['DV']['Location']:
      print rec
      periods = rec['Period']
      if type(periods) == type({}):
         periods = [periods]
      for p in periods:
         date =  p['value'][0:10]
         rep = p['Rep']
         if type(rep) == type({}):
            rep = [rep]
         for r in rep:
            hour = int(r['$'])/60
            row = empty_row.copy()
            for k in r.keys():
               row[k] = r[k]
            try:
               if row['Pt'] != 'null': row['Pt'] = "'" + row['Pt'] + "'"
               if row['D'] != 'null': row['D'] = "'" + row['D'] + "'"
               point = "ST_GeomFromText('POINT({lon} {lat})',{srid})".format(lon=rec['lon'],lat=rec['lat'], srid=srid)
               time = "to_timestamp('{date} {HH:02d}:00:00', 'YYYY-MM-DD HH24:MI:SS')".format(date=date,HH=hour)
               names = "the_geom,i,elevation,name,time,{W},{V},{T},{S},{P},{G},{D},{Pt},{Dp},{H}".format(**col_names)
               values = "{point},'{i}',{elevation},'{name}',{time},{W},{V},{T},{S},{P},{G},{D},{Pt},{Dp},{H}".format(
                  point=point,i=rec['i'],elevation=rec['elevation'], name=rec['name'], time=time, **row)
               cmd = "insert into {tbl} ({names}) VALUES ({values})".format(tbl=table_name, names=names, values=values)
               print cmd
               result = cl.sql(cmd)
            except CartoDBException as e:
               print ("some error ocurred", e)

if __name__ == '__main__':
   from sys import argv
   data = fetchObs()
   upload(argv[1], data=data )


