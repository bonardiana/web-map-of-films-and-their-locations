import folium
import pandas
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


def _input():
    """
    'None' -> int
    This function reads the year and returns it if there is data on films
    taken at that time.
    """
    while True:
        try:
            year = int(input())
            if type(year) == int:
                if year < 1874:
                    print("Too early for films.")
                elif year > 2024:
                    print("Too late for films.")
                else:
                    return year
        except:
            print("You entered not a date. Try again.")


def is_movie(line, year_index):
    """
    None->bull
    THis function checks whether it is movie or serial, TV-show
    if it is movie returns True in not False
    >>> is_movie(["Splash", "(2009)", "USA"], 1)
    True
    >>> is_movie(["Splash", "(2009)", "{seria1.1}", "USA"], 1)
    False
    >>> is_movie(["Splash", "(2009)", "{seria1.1}", "USA"], 1)
    False
    """
    if line[year_index+1].startswith("{") or line[year_index+1] == "(TV)" or line[year_index+1] == "(V)":
        return False
    else:
        return True


def is_year(el):
    """
    str-> bool
    This function checks whether element is year and returns True if it is
    in other case return False
    """
    if el.startswith("(") and el.endswith(")") and len(el) == 6:
        if "?" not in el and el[1].isdigit():
            if el[2].isdigit() and el[3].isdigit() and el[4].isdigit():
                return True
    return False


def take_corr_lines(Y, file_name):
    """
    int, str -> set
    This function reads lines from file and returns set with
    tuple(filn_title, location) with films which where made in Y tear
    """
    fall = True
    line_set = set()
    location_lst = []
    f = open(file_name, 'r', errors='ignore')
    data = f.readline()
    while not data.startswith("=="):
        data = f.readline()
    for line in f:
        try:
            l = line
            line = line.split()
            year_index = False
            for counter, el in enumerate(line):
                if is_year(el):
                    year_index = counter
                    year = int(line[year_index][1:-1])
                    break

            if year_index and year == Y:
                if is_movie(line, year_index):
                    fall = False
                    str_year = line[year_index]
                    l = tuple(l.replace(
                        "\t", "").replace("\n", "").split(str_year))
                    line_set.add(l)
        except Exception as err:
            pass
    if fall:
        print("There is to films which were made in this year")
    return line_set


def dict_of_locations(line_set):
    """
    set->dict
    This function reads set of tuples (film, locations) and transform it to the
    dict with keys = locations and values = list of films wich where made there
    """
    locations_dict = dict()
    for el in line_set:
        loc = el[1]
        if loc not in locations_dict:
            locations_dict[loc] = []
        if el[0] not in locations_dict[loc]:
            locations_dict[loc].append(el[0])
    return locations_dict


def locations_to_coordinates(dct_loc):
    """
    dct -> dct
    This functions transform dict with keys= location to the dict with
    keys =(latitude, longitude) and values = films made in that cities
    """
    to_retry = dict()
    coordinates = dict()
    for loc in dct_loc:
        l = loc.split(',')
        la = False
        lo = False
        try:
            geolocator = Nominatim(user_agent="hello_it_is_me")
            geocode = RateLimiter(geolocator.geocode, error_wait_seconds=1.0,
                                  max_retries=0, swallow_exceptions=False, return_value_on_exception=True)
            location = geolocator.geocode(l[0])
            la = location.latitude
            lo = location.longitude
        except Exception as err:
            try:
                location = geolocator.geocode(l[1])
                la = location.latitude
                lo = location.longitude
            except Exception as err2:
                print(loc)
                print(err2)
                to_retry[loc] = dct_loc[loc]
        if la and lo:
            coordinates[(la, lo)] = '| '.join(dct_loc[loc])
    return coordinates, to_retry


def color(quantity):
    """
    This function to determine the color of the icon on the map
    it returns color based on quantity of films made in that location
    """
    if 10 > quantity > 5:
        return 'orange'
    if 5 > quantity > 0:
        return 'red'
    if 20 > quantity > 10:
        return 'yellow'
    if 50 > quantity > 20:
        return 'green'
    if 100 > quantity > 50:
        return 'blue'
    else:
        return 'purple'


def to_map(coordinates, countries):
    map = folium.Map(location=[48.314775, 25.082925], zoom_start=10)
    fg_hc = folium.FeatureGroup(name="Films")
    fg_pp = folium.FeatureGroup(name="Countries")
    fg_hz = folium.FeatureGroup(name="Population")
    fg_hz.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), style_function=lambda x: {
                    'fillColor': 'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))
    for films in coordinates:
        fg_hc.add_child(folium.CircleMarker(location=[
                        films[0], films[1]], radius=10, popup=coordinates[films], fill_color='black', fill_opacity=0.7))
    for films in countries:
        number_of_films = countries[films].count('|') + 1
        fg_pp.add_child(folium.CircleMarker(location=[
                        films[0], films[1]], radius=10, popup=str(number_of_films), fill_color=color(number_of_films), fill_opacity=1))
    map.add_child(fg_hc)
    map.add_child(fg_pp)
    map.add_child(fg_hz)
    map.add_child(folium.LayerControl())
    map.save("My_Map.html")


def country_dict_of_locations(line_set):
    """
    set -> dict
    This function reads set of tuples (film, locations) and transform it to the
    dict with keys = country and values = list of films wich where made there
    """
    try:
        country_dict = dict()
        for el in line_set:
            country = el[1].split()[-1]
            if country.endswith(")"):
                country = country[:country.index("(")]
            if country not in country_dict:
                country_dict[country] = []
            country_dict[country].append(el[0])
    except:
        print(el)
    return country_dict


def countries_locations_to_coordinates(country_dict):
    """
    dct -> dct
    This functions transform dict with keys= location to the dict with
    keys = (latitude, longitude) and values = films made in that country
    """

    i = 0
    to_retry = dict()
    coordinates = dict()
    for country in country_dict:
        la = False
        lo = False
        try:
            geolocator = Nominatim(user_agent="hello_it_is_me")
            geocode = RateLimiter(geolocator.geocode, error_wait_seconds=5.0, max_retries=0,
                                  swallow_exceptions=False, return_value_on_exception=True)
            location = geolocator.geocode(country)
            la = location.latitude
            lo = location.longitude
            print(i)
            i += 1
        except Exception as err:
            print(country)
            print(err)
            to_retry[country] = country_dict[country]
        if la and lo:
            coordinates[(la, lo)] = '|'.join(country_dict[country])
    return coordinates, to_retry


def _main():
    year = _input()
    line_set = (take_corr_lines(year, file_name="locations.list.txt"))
    dct_loc = dict_of_locations(line_set)
    dct_coordinates, to_retry = locations_to_coordinates(dct_loc)
    while to_retry:
        dict2, to_retry = locations_to_coordinates(to_retry)
        dct_coordinates.update(dict2)
    country_dct_loc = country_dict_of_locations(line_set)
    country_dct_coordinates, to_retry = countries_locations_to_coordinates(
        country_dct_loc)
    while to_retry:
        country_dict2, to_retry = countries_locations_to_coordinates(
            to_retry)
        country_dct_coordinates.update(country_dict2)
    to_map(dct_coordinates, country_dct_coordinates)
    print("Your map is My_Map.html")


if __name__ == "__main__":
    _main()
