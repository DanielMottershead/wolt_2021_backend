# Backend assignment for Wolt Summer 2021 Internship.
# Created by Daniel Mottershead.
from aiohttp import web
import json
from math import sin, cos, sqrt, atan2, radians

# caluclates distance between restaurant and customer, using
# the Haversine formula.


def calculate_distance(lat_c, long_c, lat_r, long_r):
    R = 6373.0

    long_c = radians(float(long_c))
    long_r = radians(float(long_r))
    lat_c = radians(float(lat_c))
    lat_r = radians(float(lat_r))
    dlon = long_c - long_r
    dlat = lat_c - lat_r

    a = sin(dlat / 2)**2 + cos(lat_r) * cos(lat_c) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

# Ranks the results based on if the restaurant is currently online.


def rank(first_sort, sorted_online, data):
    top_10 = []
    keys = list(sorted_online.keys())
    for i in keys:
        for j in data['restaurants']:
            if(i == j['blurhash']):
                top_10.append(j)
        if(len(top_10) == 10):
            break
    if(len(top_10) < 10):
        not_online = []
        for key in list(first_sort.keys()):
            if(len(not_online) + len(top_10) == 10):
                break
            if not(key in sorted_online):
                not_online.append(first_sort[key])
        final = top_10 + not_online
    return top_10

# Sorts the restaurants based on the given parameter e.g. popularity.


def sort_data(in_range, data, order):
    first_sort = dict(
        sorted(in_range.items(), key=lambda item: item[1][0], reverse=order))
    sorted_online = {key: val for key,
                     val in first_sort.items() if val[1]}
    return rank(first_sort, sorted_online, data)

# Gets the list of restaurants based on the given request parameters


def get_data(sort_par, req, data):
    try:
        param1 = float(req.rel_url.query['lat'])
        param2 = float(req.rel_url.query['lon'])
    except ValueError:
        param1 = 0
        param2 = 0
    in_range = {}
    i = 0

    while(i < len(data['restaurants'])):
        cur = data['restaurants'][i]
        loc = cur['location']
        name = cur['name']
        online = cur['online']
        restaurant_id = cur['blurhash']
        dist = calculate_distance(param1, param2, loc[0], loc[1])
        new_par = None

        if(sort_par == 'distance'):
            new_par = dist
        elif(sort_par == 'popularity'):
            new_par = cur['popularity']
        else:
            new_par = cur['launch_date']
        if(dist <= 1.5):
            # Using blurhash as key, because there were restaurants with the
            # same name and I'm assuming blurhash is generated with a hashing
            # function so the likelyhood of collisions is small.
            in_range['{}'.format(restaurant_id)] = [new_par, online, name]
        i += 1
    return in_range

# Main function that handles the creation and combination
# of the restaurant lists.


async def handle(request):
    f = open('data.JSON',)
    data = json.load(f)
    f.close()

    pop = get_data('popularity', request, data)
    date = get_data('launch_date', request, data)
    dist = get_data('distance', request, data)
    first = {
        "title": "Popular Restaurants",
        "restaurants": sort_data(pop, data, True)
    }
    second = {
        "title": "New Restaurants",
        "restaurants": sort_data(date, data, True)
    }
    third = {
        "title": "Nearby Restaurants",
        "restaurants": sort_data(dist, data, False)
    }

    all_data = [first, second, third]
    response_obj = {'sections': all_data}
    return web.Response(text=json.dumps(response_obj))

app = web.Application()
app.router.add_get('/discovery', handle)

web.run_app(app)
