"""
Real Nepal cities, used for demo purposes across the tasks (not for the
big n=10,000 stress test in benchmark.py - obviously Nepal doesn't have
10,000 cities with usable data, so that part uses randomly generated
cities instead. This file is just for making the report/demo actually
readable with real names instead of City1, City2, etc).

Distance is rough road-distance in km from Kathmandu (city_id=0).
Coordinates and population numbers are approximate, just grabbed from
general knowledge, not pulled from an official census dataset.
"""
from city import City

NEPAL_CITIES_RAW = [
    (0,  "Kathmandu",   27.7172, 85.3240, 1_003_285, 0),
    (1,  "Pokhara",     28.2096, 83.9856,   414_141, 200),
    (2,  "Lalitpur",    27.6588, 85.3247,   293_378, 6),
    (3,  "Bhaktapur",   27.6710, 85.4298,   304_651, 13),
    (4,  "Biratnagar",  26.4525, 87.2718,   242_548, 400),
    (5,  "Birgunj",     27.0104, 84.8821,   240_922, 220),
    (6,  "Dharan",      26.8129, 87.2831,   173_990, 380),
    (7,  "Bharatpur",   27.6766, 84.4342,   280_502, 146),
    (8,  "Butwal",      27.7000, 83.4486,   139_301, 265),
    (9,  "Dhangadhi",   28.6996, 80.5966,   150_785, 615),
    (10, "Janakpur",    26.7288, 85.9247,   163_434, 220),
    (11, "Hetauda",     27.4287, 85.0322,    84_671, 135),
    (12, "Nepalgunj",   28.0500, 81.6167,   139_206, 530),
    (13, "Itahari",     26.6650, 87.2750,   125_881, 400),
    (14, "Dhulikhel",   27.6217, 85.5442,    36_827, 30),
    (15, "Ilam",        26.9088, 87.9284,    32_735, 460),
    (16, "Tansen",       27.8667, 83.5500,    32_034, 240),
    (17, "Gorkha",      28.0000, 84.6333,    28_711, 145),
    (18, "Jumla",       29.2747, 82.1838,    28_045, 490),
    (19, "Mustang",     28.9977, 83.8226,     14_452, 270),
]


def get_nepal_cities():
    return [City(*row) for row in NEPAL_CITIES_RAW]