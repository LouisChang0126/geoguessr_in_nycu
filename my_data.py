import geopandas as gpd
import osmnx as ox
import os
import requests
from tqdm import tqdm
import numpy as np
import pandas as pd
import argparse

# turn response caching off
ox.settings.use_cache = False

# turn it back on and turn on/off logging to your console
ox.settings.use_cache = True
ox.settings.log_console = False
    
    
def parser_args():
    parser = argparse.ArgumentParser(description='Setting the type of data')
    parser.add_argument('--network_type', type=str, default='walk', help='string {"all", "all_public", "bike", "drive", "drive_service", "walk"}')
    



def get_street_view_image(api_key, location, size='600x300', heading=None, fov=90, pitch='0'):
    """
    Fetches a Google Street View image.

    Parameters:
    api_key (str): Your Google Maps API key.
    location (str): A location (latitude/longitude or address) or panorama ID.
    size (str): Size of the image in WIDTHxHEIGHT format (default '600x300').
    heading (int, optional): The compass heading of the camera (0 to 360 degrees).
    fov (int, optional): Field of view of the image (default 90).
    pitch (int, optional): Up or down angle of the camera in degrees (-90 to 90).
    
    Returns:
    Image data (bytes) if successful, else error message.
    """
    base_url = 'https://maps.googleapis.com/maps/api/streetview'
    params = {
        'size': size,
        'location': location,
        'heading': heading,
        'fov': fov,
        'pitch': pitch,
        'key': api_key,
        'return_error_code': 'true'
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.content  # Return image data as bytes
    else:
        return f"Error: {response.status_code}, {response.text}"
    

if __name__ == '__main__':
    args = vars(parser_args())

    # download/model a street network for some city then visualize it
    G = ox.graph_from_place("National Yang Ming Chiao Tung University Guangfu Campus, Hsinchu, Taiwan", network_type=args['network_type'])

    # add elevation to nodes automatically, calculate edge grades, plot network
    # you need a google elevation api key to run this cell!
    google_elevation_api_key = os.environ['API_KEY']
    G = ox.elevation.add_node_elevations_google(G, api_key=google_elevation_api_key)
    G = ox.elevation.add_edge_grades(G)


    gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
    gdf_edges = gdf_edges.reset_index(drop=True)

    api_key = os.environ['API_KEY']
    data_info_list = []

    for i in tqdm(range(gdf_edges.shape[0])):
        
        line = gdf_edges.iloc[i]['geometry']
        pitch_ang = "{:.1f}".format(np.rad2deg(np.arctan(gdf_edges.iloc[1]['grade'])))
        for j in range(len(line.coords)):
            location = f'{line.coords[j][1]}, {line.coords[j][0]}' 
            for k in range(8):
                heading_angle = str(k*45.0)
                image_data = get_street_view_image(api_key, 
                                                location, 
                                                heading=heading_angle, 
                                                pitch=pitch_ang)

                data_info = pd.Series([i, j, line.coords[j], float(heading_angle), float(pitch_ang)])
                if type(image_data) == str:
                    # The error code, google doesn't have the data
                    data_info['is_error'] = True
                else:
                    data_info['is_error'] = False
                    # To save the image locally
                    with open(f'data/{location}/{heading_angle}.jpg', 'wb') as f:
                        f.write(image_data)

                data_info_list.append(data_info)


    df = pd.DataFrame(np.array(data_info_list),
                    columns=['path_id', 'spot_id', 'coords', 'heading', 'pitch', 'is_error'])

    df.to_csv('data_info.csv')
