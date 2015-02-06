#!/usr/bin/env python
# usage: create_obs_table new_table_name
# WARNING: If table already exists it will be deleted and recreated, all rows and new or modified column are lost!

from create import create

columns = ["name text",
           "i text",
           "elevation float8",
           "time timestamptz",
           "weather_type text",
           "visibility float8",
           "temperature float8",
           "wind_speed float8",
           "pressure float8",
           "wind_gust text",
           "wind_direction text",
           "pressure_tendency text",
           "dew_point float8",
           "screen_relative_humidity float8"]

if __name__ == '__main__':
    from sys import argv
    create( argv[1],  ",".join( columns ) )

