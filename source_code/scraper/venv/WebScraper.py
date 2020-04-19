import NetworkUtil
import CustomConstants
import CustomUtil

class WebScraper:

    def start_scraping(self):
        CustomUtil.clear_all_files()
        CustomConstants.URL_TO_BE_VISITED.add(CustomConstants.URL_TO_BE_CRAWLED)
        html_response = NetworkUtil.read_from_network(CustomConstants.URL_TO_BE_VISITED.pop())
        if html_response == CustomConstants.URL_IS_NOT_VALID:
            print(CustomConstants.URL_IS_NOT_VALID_MSG)
        elif html_response == CustomConstants.ERROR_OCCURED_WHILE_SENDING_REQUEST:
            print(CustomConstants.ERROR_OCCURED_WHILE_SENDING_REQUEST_MSG)
        else:
            room_detail_list = CustomUtil.extract_data(html_response)
            if len(room_detail_list) > 0:
                CustomUtil.write_data_into_file(CustomConstants.JSON_DATA_FILE_NAME, room_detail_list)
                room_detail_list = CustomUtil.read_file(CustomConstants.JSON_DATA_FILE_NAME)
                city_list = CustomUtil.get_city_list(room_detail_list)

                for city in city_list:
                    city_room_detail_list = CustomUtil.get_city_data(city,room_detail_list)
                    room_capacity_list = CustomUtil.get_room_capacity_list(city_room_detail_list)
                    CustomUtil.print_analysis(city,room_capacity_list,city_room_detail_list)

if __name__ == "__main__":
    WebScraper().start_scraping()
