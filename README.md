# MYCU Street View

## Set up the api key
Get the api key from the google map api:
https://developers.google.com/maps/documentation/streetview?hl=zh-tw


## Run 
```
pip install -r requirements.txt
python3 my_data.py --network_type walk
```

## How the Data stored
* Every spot on the map has the 8 piture heading different direction
* Here is how data stored:
```
data/
├── coordinate_1/
│   ├── 0.0.jpg
│   ├── 45.0.jpg
|   ├── 90.0.jpg
|   ├── 135.0.jpg
|   ├── 180.0.jpg
|   ...
│   └── 315.jpg
|
├── coordinate_2/
|   ├── 0.0.jpg
|   ...
│   └── 315.jpg
...


```