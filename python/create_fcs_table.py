#!/usr/bin/env python
# usage: create_fcs_table new_table_name
# WARNING: If table already exists it will be deleted and recreated, all rows and new or modified column are lost!

from create import create

columns = ["name text",
           "i text",
           "elevation float8",
           "time timestamptz",
           "max_uv_index float8",
           "weather_type text",
           "visibility text",
           "temperature float8",
           "wind_speed float8",
           "precipitation_probability float8",
           "wind_gust float8",
           "wind_direction text",
           "feels_like_temperature float8",
           "screen_relative_humidity float8"]

if __name__ == '__main__':
    from sys import argv
    create( argv[1],  ",".join( columns ) )

