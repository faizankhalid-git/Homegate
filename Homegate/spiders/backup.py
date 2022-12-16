# import json
#
# import scrapy
# from scrapy import Request
#
#
# class HomegateSpider(scrapy.Spider):
#     name = 'homegate'
#     # custom_settings = {
#     #     'FEED_URI': 'homegate.csv',
#     #     'FEED_FORMAT': 'csv',
#     # }
#     zyte_key = '07a4b6f903574c1d8b088b55ff0265fc'  # Todo : YOUR API KEY FROM ZYTE
#     custom_settings = {
#         'FEED_URI': 'homegate.csv',
#         'FEED_FORMAT': 'csv',
#         'ZYTE_SMARTPROXY_ENABLED': True,
#         'ZYTE_SMARTPROXY_APIKEY': zyte_key,
#         'DOWNLOADER_MIDDLEWARES': {
#             'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610
#         },
#     }
#     url = "https://api.homegate.ch/search/listings"
#
#     payload = {
#         "query": {
#             "offerType": "RENT",
#             "categories": [
#                 "APARTMENT",
#                 "MAISONETTE",
#                 "DUPLEX",
#                 "ATTIC_FLAT",
#                 "ROOF_FLAT",
#                 "STUDIO",
#                 "SINGLE_ROOM",
#                 "TERRACE_FLAT",
#                 "BACHELOR_FLAT",
#                 "LOFT",
#                 "ATTIC",
#                 "HOUSE",
#                 "ROW_HOUSE",
#                 "BIFAMILIAR_HOUSE",
#                 "TERRACE_HOUSE",
#                 "VILLA",
#                 "FARM_HOUSE",
#                 "CAVE_HOUSE",
#                 "CASTLE",
#                 "GRANNY_FLAT",
#                 "CHALET",
#                 "RUSTICO",
#                 "SINGLE_HOUSE",
#                 "HOBBY_ROOM",
#                 "CELLAR_COMPARTMENT",
#                 "ATTIC_COMPARTMENT"
#             ],
#             "excludeCategories": [
#                 "FURNISHED_FLAT"
#             ],
#             "location": {
#                 "geoTags": [
#                     "geo-city-zurich"
#                 ]
#             }
#         },
#         "sortBy": "listingType",
#         "sortDirection": "desc",
#         "from": 0,
#         "size": 20,
#         "trackTotalHits": True,
#         "fieldset": "srp-list"
#     }
#     headers = {
#         'authority': 'api.homegate.ch',
#         'accept': 'application/json, text/plain, */*',
#         'accept-language': 'en-US,en;q=0.9,de;q=0.8',
#         'cache-control': 'no-cache',
#         'content-type': 'application/json',
#         'origin': 'https://www.homegate.ch',
#         'pragma': 'no-cache',
#         'referer': 'https://www.homegate.ch/',
#         'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Linux"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'same-site',
#         'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
#     }
#
#     def start_requests(self):
#         yield Request(self.url, headers=self.headers, body=json.dumps(self.payload), method='POST', meta={'from': 0})
#
#     def parse(self, response, **kwargs):
#         json_data = json.loads(response.text)
#         listings = json_data.get('results', {})
#         for listing in listings:
#             yield Request(
#                 url=f"https://api.homegate.ch/listings/listing/{listing.get('id', '')}?sanitize=true",
#                 callback=self.detail_page,
#                 meta={'id': listing.get('id', '')}
#             )
#
#         from_list = response.meta['from'] + 20
#         total_pages = json_data.get('total', '')
#         if from_list < total_pages:
#             self.payload['from'] = from_list
#         yield Request(url=self.url,
#                       headers=self.headers,
#                       body=json.dumps(self.payload),
#                       method='POST',
#                       meta={'from': from_list},
#                       callback=self.parse)
#
#     def detail_page(self, response):
#         json_data = json.loads(response.text).get('listing', {})
#         characteristics = json_data.get('characteristics', {})
#         floor = characteristics.get('floor', {})
#         distance_transport = characteristics.get('distancePublicTransport', {})
#         rooms = characteristics.get('numberOfRooms', {})
#         living_space = characteristics.get('livingSpace', {})
#         has_garage = characteristics.get('hasGarage', {})
#         is_minergie_general = characteristics.get('isMinergieGeneral', {})
#         is_new_building = characteristics.get('isNewBuilding', {})
#
#         images = json_data.get('localization', {}).get('de', {}).get('attachments', {})
#         building_images = [image.get('url', '') for image in images]
#
#         address = json_data.get('address', {})
#         prices = json_data.get('prices', {}).get('rent', {})
#
#         title_desc = json_data.get('localization', {}).get('de', {}).get('text', {})
#         yield {
#             'Title': title_desc.get('title', ''),
#             'Floor': floor,
#             'Rooms': rooms,
#             'Living Space': living_space,
#             'Images': ', '.join(building_images),
#             'Country': address.get('country', ''),
#             'Locality': address.get('locality', ''),
#             'PostalCode': address.get('postalCode', ''),
#             'Region': address.get('region', ''),
#             'Street': address.get('street', ''),
#             'Distance Public Transport': distance_transport,
#             'hasGarage': has_garage,
#             'Is Minergie General': is_minergie_general,
#             'Is New Building': is_new_building,
#             'Extra cost': prices.get('extra', ''),
#             'Gross cost': prices.get('gross', ''),
#             'Net cost': prices.get('net', ''),
#             'Description': title_desc.get('description', ''),
#             'Url': f"https://www.homegate.ch/mieten/{response.meta['id']}",
#             'json':response.text
#         }
