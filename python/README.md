# Python utilities and examples

## create.py

## create_fcs_table.py

## create_obs_table.py

## describe.py

## drop.py

## truncate.py

## upload_fcs.py

Download a UK weather forecast data and upload as rows in specified CartoDB table. Any existing rows will be deleted before upload starts.

## upload_obs.py

Download latest UK weather observation data and upload as rows in specified CartoDB table. Any existing rows will be deleted before upload starts.

# Set up

Register for CartoDB and Datapoint and using my_keys.py.in as template copy your API keys to my_keys.py

# Examples

```
python create_obs_table.py uk_weather_obs
python upload_obs.py uk_weather_obs
```