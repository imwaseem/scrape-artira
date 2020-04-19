import CustomConstants
from validator_collection import checkers
import  requests
from urllib.parse import urljoin


def get_absolute_url(relative_url):
    return  urljoin(CustomConstants.URL_TO_BE_CRAWLED,relative_url)

def read_from_network(url):
    try:
        if checkers.is_url(url):
            response = requests.get(url, headers=CustomConstants.REQUEST_HEADER)
            CustomConstants.URL_VISITED.add(url)
            return response
        else:
            CustomConstants.URL_TO_BE_VISITED.add(url)
            return  CustomConstants.URL_IS_NOT_VALID
    except:
        CustomConstants.URL_TO_BE_VISITED.add(url)
        return CustomConstants.ERROR_OCCURED_WHILE_SENDING_REQUEST

