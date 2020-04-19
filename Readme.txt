1)To run this program make sure that you imported all the required packages with same version mentioned in requirements.txt
2)Run WebScraper.py class
Note programe takes time to complete it execution because there are many requests.
3)output of task 1 will be written in json_data.txt 

Assumption:from the data i collected in task 1.i didn't have a city name seperately. so i fetched it from location string for every data.
i assume that two words after 'street' or 'st' or 'Rd' is a name of city.

for example:in "50 La Trobe Street Melbourne VIC 3000" city name is  'Melbourne VIC'

