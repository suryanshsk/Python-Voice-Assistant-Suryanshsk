import folium
import matplotlib.pyplot as plt
import numpy as np
from geopy.geocoders import Nominatim

def get_location_coordinates(area_name):
    geolocator = Nominatim(user_agent="Planting_Analysis")  
    try:
        location = geolocator.geocode(area_name)
        if location:
            return location.latitude, location.longitude
        else:
            print("Area not found")
            return None, None
    except Exception as e:
        print(f"Error occurred while fetching coordinates: {e}")
        return None, None

def interactive_map(lat, lon, area_name):
    area_map = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker([lat, lon], popup=f"{area_name}").add_to(area_map)
    
    map_filename = f"{area_name}_map.html"
    area_map.save(map_filename)
    print(f"Interactive map saved as {map_filename}")
    return map_filename

def trees_capacity(area_km2, tree_species):
    species_density = {
        "Oak": 200,
        "Pine": 300,
        "Maple": 150,
        "Cedar": 250,
        "Birch": 180,
        "Willow": 220,
        "Spruce": 260,
        "Fir": 240,
        "Aspen": 190,
        "Cherry": 200,
        "Magnolia": 170,
        "Redwood": 150,
        "Palms": 100,
        "Teak": 120,
        "Bamboo": 300,
    }
    if tree_species in species_density:
        trees_per_km2 = species_density[tree_species]
    else:
        trees_per_km2 = 100  # default density
    total_trees = area_km2 * trees_per_km2
    return total_trees

def oxygen_output(trees, tree_species):
    species_oxygen = {
        "Oak": 180,
        "Pine": 140,
        "Maple": 150,
        "Cedar": 170,
        "Birch": 160,
        "Willow": 155,
        "Spruce": 150,
        "Fir": 140,
        "Aspen": 145,
        "Cherry": 160,
        "Magnolia": 170,
        "Redwood": 150,
        "Palms": 50,
        "Teak": 120,
        "Bamboo": 75,
    }
    oxygen_per_tree = species_oxygen.get(tree_species, 118) 
    total_oxygen = trees * oxygen_per_tree
    return total_oxygen


def planting_recommendations(area_name):
    
    recommendations = {
        "tropical": ["Teak", "Bamboo", "Palm"],
        "temperate": ["Oak", "Maple", "Cherry"],
        "arid": ["Cedar", "Willow", "Fir"],
        "coastal": ["Birch", "Magnolia", "Redwood"],
    }
    
    if "tropical" in area_name.lower():
        return recommendations["tropical"]
    elif "arid" in area_name.lower():
        return recommendations["arid"]
    elif "coastal" in area_name.lower():
        return recommendations["coastal"]
    else:
        return recommendations["temperate"]

def carbon_offset(trees):
    carbon_per_tree = 22
    total_offset = trees * carbon_per_tree
    return total_offset

def visualize_results(tree_capacity, oxygen_output_val, tree_species):
    labels = ['Trees', 'Oxygen Output (kg)']
    values = [tree_capacity, oxygen_output_val]
    
    x = np.arange(len(labels))  
    width = 0.35 

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, values, width, label='Values')

    ax.set_ylabel('Count / Output')
    ax.set_title('Tree Capacity and Oxygen Output')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    for rect in rects1:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.show()

def analyze_area_for_tree(area_name, area_km2, tree_species):
    lat, lon = get_location_coordinates(area_name)
    if lat is None or lon is None:
        return

    map_file = interactive_map(lat, lon, area_name)

    tree_capacity = trees_capacity(area_km2, tree_species)
    oxygen_output_val = oxygen_output(tree_capacity, tree_species)
    carbon_offset_val = carbon_offset(tree_capacity)
    suitable_trees = planting_recommendations(area_name)

    print(f"For the area of {area_km2} km² in {area_name}: ")
    print(f"Estimated number of {tree_species} trees that can be planted: {tree_capacity}")
    print(f"Estimated annual oxygen output: {oxygen_output_val} kg")
    print(f"Estimated carbon offset: {carbon_offset_val} kg/year")
    print(f"View the interactive map here: {map_file}")
    print(f"Recommended tree species for planting: {', '.join(suitable_trees)}")

    visualize_results(tree_capacity, oxygen_output_val, tree_species)

if __name__ == "__main__":
    area_name = input("Enter the name of the city/Area Name: ")
    area_km2 = float(input("Enter the area in km²: "))
    tree_species = input("Enter the tree species (e.g. Oak, Pine, Maple, Cedar, Cherry etc): ")
    analyze_area_for_tree(area_name, area_km2, tree_species)
