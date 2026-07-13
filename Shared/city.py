"""
Basic city record, used by every data structure in task 1 (and reused in
task 2 for the graph nodes too).

city_id is what BST/AVL/HashTable key on, distance is what MinHeap sorts
by. Everything else (name, coords, population) is just payload that
rides along.
"""

class City:
    def __init__(self, city_id, name, lat, lon, population, distance):
        self.city_id = city_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.population = population
        self.distance = distance  # km from a fixed reference point (Kathmandu)

    def __repr__(self):
        return f"City({self.city_id}, {self.name}, dist={self.distance}km)"