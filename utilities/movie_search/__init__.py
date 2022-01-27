
import requests

omdb_api_key = '46c25f22'
omdb_api_url = 'https://omdbapi.com'
def search_movie(title,page):
    url= f'{omdb_api_url}/'
    url_parameter = {
        's':title,
        'plot':'full',
        'apikey':omdb_api_key,
        'page':page
    }
    response = requests.get(url,params=url_parameter)
    return response.json()['Search']

