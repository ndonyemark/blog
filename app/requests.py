import urllib.request, json
from .models import Quotes

base_url=None

def configure_request(app):
    global base_url
    base_url = app.config["API_BASE_URL"]
    print(base_url)

def get_quotes():

    with urllib.request.urlopen(base_url) as url:

        quotes_data = url.read()
        print(quotes_data)
        quotes_response = json.loads(quotes_data)
        return quotes_response

#         quote_results = None

#         if quote_results:
#             quote_results_list = quote_results
#             print(quote_results)
#             quote_results = process_results(quote_results_list)
    
#     return quote_results

# def process_results(quotes_list):

#     quotes_results = []

#     for quote_item in quotes_list:
#         author = quote_item.get('author')
#         quote = quote_item.get('quote')
#         permalink = quote_item.get('permalink')

#         if quote:
#             quote_object = Quotes(author, quote, permalink)
#             quotes_results.append(quote_object)
    
#     return quotes_results