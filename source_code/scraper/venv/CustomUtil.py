from bs4 import BeautifulSoup
import CustomConstants
import NetworkUtil
from validator_collection import checkers
from os import path
import time
from RoomDetail import RoomDetail
import  json
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def parse_html_content(content):
    return BeautifulSoup(content, 'html.parser')


def extract_data(html_page):
    temporary_variable = ''
    parsed_html_page = parse_html_content(html_page.content)
    links = parsed_html_page.find_all('a')

    for link in links:
        if link.get('href') == '/locations/':
            temporary_variable = link.get('href')
            break

    if temporary_variable != '' and (not checkers.is_url(temporary_variable)):
        CustomConstants.URL_TO_BE_VISITED.add(NetworkUtil.get_absolute_url(temporary_variable))
    else:
        return CustomConstants.SOMETHING_WENT_WRONG_WHILE_FETCHING_LOCATIONS

    html_page = NetworkUtil.read_from_network(CustomConstants.URL_TO_BE_VISITED.pop())
    parsed_html_page = parse_html_content(html_page.content)
    location_cards = parsed_html_page.find_all(class_='location card')

    if len(location_cards) > 0:
        clear_set_data()

    for location_card in location_cards:
        link = location_card.get('href')
        if checkers.is_url(link):
            CustomConstants.URL_TO_BE_VISITED.add(link)
        else:
            link = NetworkUtil.get_absolute_url(link)
            CustomConstants.URL_TO_BE_VISITED(link)

    room_links = set()

    for location in CustomConstants.URL_TO_BE_VISITED:
        html = NetworkUtil.read_from_network(location)
        parsed_html = parse_html_content(html.content)
        room_links.update(extract_rooms_feed(parsed_html))
        time.sleep(3.0)

    clear_set_data()

    room_detail_list = list()

    for room_link in room_links:
        html_page = NetworkUtil.read_from_network(room_link)
        parsed_html_page = parse_html_content(html_page.content)
        room_detail = extract_room_detail(parsed_html_page)
        room_detail_list.append(room_detail)
        time.sleep(3.0)
    return room_detail_list


def clear_set_data():
    CustomConstants.URL_TO_BE_VISITED.clear()
    CustomConstants.URL_VISITED.clear()

def write_into_file(file_name, data):
    if not path.isfile(file_name):
        with open(file_name, 'w') as file:
            for line in data:
                file.write(line + '\n')
    else:
        with open(file_name,'a') as file:
            for line in data:
                file.write(line + '\n')


def write_into_file_test(file_name, data):
    if not path.isfile(file_name):
        with open(file_name, 'w') as file:
            for line in data:
                file.write(line.location + '\n')
    else:
        with open(file_name,'a') as file:
            for line in data:
                file.write(line.location + '\n')

def write_data_into_file(file_name,data):
    if not path.isfile(file_name):
        with open(file_name,'w') as file:
            file.write(json.dumps([ob.__dict__ for ob in data],indent = 2, separators=(',', ': ')))
    else:
        with open(file_name, 'a') as file:
            file.write(json.dumps([ob.__dict__ for ob in data],indent = 2, separators=(',', ': ')))


def extract_rooms_feed(html_page):
    rooms = html_page.findChildren(class_='card__room')
    room_links = set()
    for room in rooms:
        room_links.add(room.find('a').get('href'))
    return room_links

def extract_room_detail(html_page):
    building_name = html_page.find(class_='room__location--title')
    price = html_page.find(class_='room__sidebar--rate-base')
    room_name = html_page.find(class_='room__title')
    address = html_page.find(class_='address')
    address = address.findChildren()
    location = ''
    capacity_of_persons = html_page.find(class_='room__sidebar--icons')
    capacity_of_persons = capacity_of_persons.find('li').get_text()

    for iterator in address:
        location = location + iterator.get_text()

    room_features = []
    room_features = extract_room_features(html_page.find(class_= 'room__features'))
    return RoomDetail(price.get_text(),capacity_of_persons,room_features,room_name.get_text(),building_name.get_text(),location)

def extract_room_features(parsed_html):
    features = parsed_html.find_all('p')
    room_features = []
    for feature in features:
        room_features.append(feature.get_text())
    return  room_features


def clear_all_files():
    clear_file(CustomConstants.JSON_DATA_FILE_NAME)



def clear_file(file_name):
    if path.isfile(file_name):
        with open(file_name,'w'):
            pass


def read_file(file_name):
    room_detail_list = list()
    with open (file_name,'r') as file :
        data = json.loads(file.read())
        for room_detail in data:
            room_detail_list.append(RoomDetail(**room_detail))

    return room_detail_list

def get_city_list(room_detail_list):
    city = set ()
    for room_detail in room_detail_list:
        location = room_detail.location.split(' ')
        index = -1
        for value in location:
            if value == 'St' or value == 'Street' or value == 'Rd':
                index = location.index(value)
                break
        city.add(location[index+1] + ' ' +location[index+2])
    return  city

def get_city_data(city_name,room_detail_list):
    city_room_detail = []
    for room_detail in room_detail_list:
        if city_name in  room_detail.location:
            city_room_detail.append(room_detail)
    return city_room_detail


def get_room_capacity_list(room_detail_list):
    room_capacity_list = set()
    for room_detail in room_detail_list:
        room_capacity_list.add(room_detail.capacity_of_persons)
    return room_capacity_list

def print_analysis(city_name,persons_capacity_list,city_room_detail_list):
    print_horizontal_line()
    avg_price_list = []
    for person_capacity in persons_capacity_list:
        price_sum = 0
        number_of_rooms = 0
        for city_room_detail in city_room_detail_list:
            if person_capacity == city_room_detail.capacity_of_persons:
                number_of_rooms = number_of_rooms + 1
                price_sum = price_sum + int(city_room_detail.price)

        if number_of_rooms > 0  and price_sum > 0:
            avg = price_sum/number_of_rooms
            print (city_name + ':' + ' $' + str(int(avg)) + ' for ' +person_capacity+' person Room')
            avg_price_list.append(avg)

    draw_bar_chart(city_name,persons_capacity_list,avg_price_list)


def draw_bar_chart(city,person_capacity_list,avg_price_list):
    # objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
    y_pos = np.arange(len(person_capacity_list))
    plt.bar(y_pos, avg_price_list, align='center', alpha=0.5)
    plt.xticks(y_pos, person_capacity_list)
    plt.ylabel('price($)')
    plt.xlabel('capacity of person')
    plt.title(city)
    plt.show()


def print_horizontal_line():
    print('_________________________________________________________________________________________________________________________________________________')