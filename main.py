import streamlit as st
import osmnx as ox
import networkx as nx

# --- Functions ---

def get_map_data(c_pt, radius_val):
    # Fetch Data from OSM
    graph = ox.graph_from_point(c_pt, dist=radius_val, network_type="drive")
    return graph

def find_shortest_route(graph, o_pt, d_pt):
    # Calculate Nodes and Route
    n1 = ox.nearest_nodes(graph, X=o_pt[1], Y=o_pt[0])
    n2 = ox.nearest_nodes(graph, X=d_pt[1], Y=d_pt[0])
    route = nx.shortest_path(graph, n1, n2, weight="length")
    
    # Calculate distance
    route_gdf = ox.routing.route_to_gdf(graph, route, weight="length")
    route_distance = int(route_gdf['length'].sum())
    
    return route, route_distance

def plot_the_map(graph, route, calculated_node_size):
    # Plotting Logic
    fig, ax = ox.plot_graph_route(
        graph, route, 
        node_size=calculated_node_size, 
        node_color="crimson", 
        route_color="black", 
        edge_linewidth=1, 
        bgcolor="white",
        show=False, close=False
    )
    return fig

# --- Main App Interface ---

st.title("Shortest Route Finder")

# Inputs
center = st.text_input("Map Center (lat, lon)", "51.5839, 4.9240")
origin = st.text_input("Start Point (lat, lon)", "51.5839, 4.9240")
dest = st.text_input("End Point (lat, lon)", "51.5925, 4.9015")
radius_val = st.number_input("Search Radius (meters)", value=2000, step=100)

try:
    # Convert text strings to tuples
    c_pt = tuple(map(float, center.split(',')))
    o_pt = tuple(map(float, origin.split(',')))
    d_pt = tuple(map(float, dest.split(',')))

    # Use Functions
    graph = get_map_data(c_pt, radius_val)
    route, route_distance = find_shortest_route(graph, o_pt, d_pt)
    
    # Dynamic Node Size Calculation
    calculated_node_size = max(5, int(30000 / radius_val))

    st.success(f"Route found! Total distance: {route_distance} meters.")

    # Display Plot
    fig = plot_the_map(graph, route, calculated_node_size)
    st.pyplot(fig)

except Exception as e:
    st.warning(f"Check your inputs! (Error: {e})")