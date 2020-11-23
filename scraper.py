# Importing needed modules
from bs4 import BeautifulSoup
import lxml
import requests
import unicodedata

monitors_url = 'https://www.czc.cz/monitory/produkty'
monitors_wa_url = 'https://www.czc.cz/sirokouhle-monitory/produkty'
mice_url = 'https://www.czc.cz/mysi/produkty'
ups_accessories_url = 'https://www.czc.cz/prislusenstvi-zalozni-zdroje-ups/produkty'

'''
Function requires two arguments: selenium webdriver and the url of a category, that will be scraped.
First the number of pages is scraped from the first page, the the function iterates through all the
pages and returns the list of individual urls for each page.
'''
def create_page_urls(category_url):

	# Scraping the number of pages with BS
	raw_scrape = requests.get(category_url).text
	soup = BeautifulSoup(raw_scrape, 'lxml')
	num_pages = soup.find('div', class_ = 'paging ajax').find('a', class_ = 'last').text
	num_pages = int(num_pages)

	# Generate a list of urls with different pages
	offset = 0
	url_list = []

	for page in range(num_pages):
		url_list.append(category_url + f'?q-first={offset}')
		offset += 27		# Number of products displayed on one page on the site

	return url_list

url_list = create_page_urls('https://www.czc.cz/skrine/produkty')

	
'''
Pipeline function for extracting the name of the product and the price assosiated. Each product is displayed
in a html element with name "tile". There are 3 tiles per row displayed on the website.
Pipeline iterates through each row of tiles and for each tile it scrapes the product name and the price.
'''
def scrape_data(url_list):
	raw_scrape = requests.get(url_list[0]).text
	soup = BeautifulSoup(raw_scrape, 'lxml')
	category_name = soup.find('div', class_ = 'entry-header').find('h1').text
	category_name = category_name[0 : -1].replace(' ', '_').replace(',', '')

	scrape = []

	for url in range(len(url_list)):	
		raw_scrape = requests.get(url_list[url]).text
		soup = BeautifulSoup(raw_scrape, 'lxml')

		tile_rows = soup.find_all('div', class_ = 'new-tile-row')

		for tile_row in tile_rows:
			tiles = tile_row.find_all('div', class_ = 'new-tile')

			for tile in tiles:
				product_name = tile.find('div', class_ = 'tile-title')
				product_name = product_name.h5.a.text

				# Getting rid of the unnecessary characters
				product_name = product_name[0 : -25]		# There's a newline character and 24 whitespaces after each product name, the amount is consistent...

				total_price = tile.find('div', class_ = 'total-price')

				try:
					sale_price = total_price.find('span', class_ = 'price action')	# I had to change a variable name so that the except statement would work
					total_price = sale_price.find('span', class_ = 'price-vatin').text

				except:
					try:
						total_price = total_price.find('span', class_ = 'price alone')
						total_price = total_price.find('span', class_ = 'price-vatin').text

					except:
						total_price = 0
						scrape.append([product_name, total_price])
						continue

				total_price = unicodedata.normalize('NFKD', total_price)
				total_price = total_price[0 : -4]				# ' Kč' after each price number, apparently 'č' character counts for 2, that's why -4
				total_price = total_price.replace(' ', '')		# So I can then convert to integer
				total_price = int(total_price)

				scrape.append([product_name, total_price])

	return scrape, category_name

scrape, categ = scrape_data(url_list)
print(scrape)
