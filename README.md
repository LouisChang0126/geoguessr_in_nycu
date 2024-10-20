# NYCU Street View

Link of our slides: https://www.canva.com/design/DAGTv0zmQag/-VYrP7rilhEdu7TqMi0n3g/edit?utm_content=DAGTv0zmQag&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

## Structure
```
geoguessr_in_nycu/
|
├── get data/ : download data from google street view
|
├── data/ : place to store data ( random angles )
├── data3/ : place to store data ( each 45 angles )
|
├── Gemini/ : use few shot to classify data into buildings
|
├── Line bot/ : webhook of line bot
|
├── building_map/ : text map to go to destination
...

```


## Set up the api key
Get the api key from the google map api:
https://developers.google.com/maps/documentation/streetview?hl=zh-tw


## Run 
```
pip install -r requirements.txt
python3 my_data.py --network_type walk
```

