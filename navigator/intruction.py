import osmnx as ox
import networkx as nx
import math
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

import google.generativeai as genai

class Instructor:
    def __init__(self):
        place = "National Yang Ming Chiao Tung University Guangfu Campus, Hsinchu, Taiwan"
        
        # # Download the street network graph for the area
        self.G = ox.graph_from_place(place, network_type="walk")
        # self.G = ox.load_graphml('NYCU.graphml')
        
        tags = {"building": True}
        gdf_building = ox.features_from_place(place, tags)
        gdf_building = gdf_building[gdf_building['name'].notna()]
        
        # Assuming gdf_filtered is a GeoDataFrame containing the buildings with their geometries
        # Ensure the CRS of the buildings matches the graph (usually it's EPSG:4326 for OSM data)
        self.gdf_bf = gdf_building.to_crs(epsg=4326)


        # Get edge geometries for the route
        self.nodes, self.edges = ox.graph_to_gdfs(self.G)
        
    def navigator(self, orig:str, dest:str):
        orig_osmid = self.search_the_osmid(orig)
        dest_osmid = self.search_the_osmid(dest)
        print(orig_osmid, dest_osmid)
        assert (orig_osmid is not None)&(dest_osmid is not None), ""
        route = ox.shortest_path(self.G, orig_osmid, dest_osmid, weight="length")
        print(route)
        # Get node degrees to find intersections
        node_degrees = dict(self.G.degree())
        intersections = [node for node, degree in node_degrees.items() if degree >= 3]
        # List to hold turn-by-turn instructions and turn locations
        turn_instructions = []
        turn_info = []
        turn_spots = []  # For storing coordinates of the turns for plotting
        # Iterate through the route, looking for turns only at intersections
        passed_inter = 0
        for i in range(1, len(route) - 1):
            if route[i] in intersections:  # Only process if the current node is an intersection
                p1 = (self.G.nodes[route[i - 1]]['y'], self.G.nodes[route[i - 1]]['x'])
                p2 = (self.G.nodes[route[i]]['y'], self.G.nodes[route[i]]['x'])
                p3 = (self.G.nodes[route[i + 1]]['y'], self.G.nodes[route[i + 1]]['x'])
                angle = self.calculate_angle(p1, p2, p3)
                if 45 < angle < 135:  # Right turn
                    turn_instructions.append(f"Turn right at intersection {route[i]}, after passing {passed_inter} intersections")
                    passed_inter = 0
                    turn_spots.append((p2[0], p2[1]))
                    turn_info.append(self.get_nearby_building((p2[0], p2[1])))
                elif 225 < angle < 315:  # Left turn
                    turn_instructions.append(f"Turn right at intersection {route[i]}, after passing {passed_inter} intersections")
                    passed_inter = 0
                    turn_spots.append((p2[0], p2[1]))
                    turn_info.append(self.get_nearby_building((p2[0], p2[1])))
                else:
                    passed_inter+=1
                
        fig, ax = ox.plot_graph_route(G, route, route_color="y", route_linewidth=1, node_size=0)
        fig.savefig("route_plot.png", dpi=300, bbox_inches='tight')      
        return self.gemini(turn_instructions, turn_info, orig, dest)
        
    def search_the_osmid(self, key):
        search_result = self.gdf_bf.loc[self.gdf_bf['name']==key]
        if search_result.empty:
            return  None
        else:
            geo = search_result['geometry']
            result_coord = list(geo.exterior.iloc[0].coords)[0]
            return ox.distance.nearest_nodes(self.G, X=result_coord[0], Y=result_coord[1])
        
    
    
    # Function to calculate angle between two vectors (for turning detection)
    def calculate_angle(self, p1, p2, p3):
        v1 = (p2[0] - p1[0], p2[1] - p1[1])
        v2 = (p3[0] - p2[0], p3[1] - p2[1])
        angle = math.degrees(math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0]))
        angle = (angle + 360) % 360  # Normalize to 0-360 degrees
        return angle


    def get_nearby_building(self, turn_spot):
       
        # Create a GeoDataFrame from the intersections
        intersection_points = [Point(x, y) for y, x in [turn_spot]]  # Create Point geometries for intersections
        gdf_intersections = gpd.GeoDataFrame(geometry=intersection_points, crs="EPSG:4326")
        
        # Perform a spatial join to find nearest buildings within a certain distance (e.g., 50 meters)
        # buffer() creates a radius around the intersection points
        buffered_intersections = gdf_intersections.copy()
        buffered_intersections['geometry'] = buffered_intersections.geometry.buffer(0.0003)  # Approx. 50 meters in degrees
        
        # Find buildings that intersect with these buffered areas (i.e., within 50 meters)
        nearby_buildings = gpd.sjoin(self.gdf_bf, buffered_intersections, how='inner', predicate='intersects')
        
        return list(nearby_buildings['name'])
        
        
    def gemini(self, turn_ins, turn_info, orig, dest):
        bf = pd.read_csv('building_feature.csv')
        print(bf.shape)
        model = genai.GenerativeModel("gemini-1.5-flash")
        SYS_PROMPT = """
        你是交通大學校園的導覽小幫手，你要做的事是從提供的路徑步驟指示引導使用者在校園中走到需要的路，請你詳細的描述每個轉彎的資訊包含第幾路口轉彎、
        轉彎的方向以及路口鄰近的建築物的名稱與大致外觀的描述，請你引導使用著到達目的地，並請遵守以下幾點：
        1. 條列式的簡述路徑步驟，不可以有過多冗長的內容
        2. 不可以擅自新增沒有提供的資訊
        3. 生成的內容請不要包含路口的編號
        """
        for i in range(len(turn_ins)):
            inst = f"路徑步驟{i}:{turn_ins[i]}, 路口鄰近的建築物資訊:"
            
            for info in turn_info[i]:

                bf_1 = bf.loc[bf['name'] == info]
                
                inst+=f"名稱：{info}描述：{bf_1['description'].iloc[0]}"
            SYS_PROMPT += inst
        response = model.generate_content(SYS_PROMPT+f"起點：{orig}終點：{dest}")
        print(response.text)
        return response.text

if __name__ == '__main__':
    inst = Instructor()
    inst.navigator('游泳館', '工程二館')
