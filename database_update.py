from scraper import scrape_data, create_page_urls
import sqlite3

urls_list = [
		'https://www.czc.cz/procesory/produkty',
		'https://www.czc.cz/zakladni-desky/produkty',
		'https://www.czc.cz/graficke-karty/produkty',
		'https://www.czc.cz/operacni-pameti/produkty',
		'https://www.czc.cz/disky/produkty',
		'https://www.czc.cz/skrine/produkty',
		'https://www.czc.cz/zdroje/produkty',
		'https://www.czc.cz/rozsirujici-karty/produkty',
		'https://www.czc.cz/chladice/produkty',
		'https://www.czc.cz/monitory/produkty',
		'https://www.czc.cz/mysi/produkty',
		'https://www.czc.cz/tiskarny-a-naplne/produkty',
		'https://www.czc.cz/klavesnice/produkty',
		'https://www.czc.cz/sluchatka-a-mikrofony/produkty',
		'https://www.czc.cz/reproduktory/produkty',
		'https://www.czc.cz/pametove-karty/produkty',
		'https://www.czc.cz/flash-disky/produkty'
]

for url in urls_list:
	scraped_list, table_name = scrape_data(create_page_urls(url))

	conn = sqlite3.connect('database.db')
	c = conn.cursor()

	try:
		c.execute(f''' CREATE TABLE {table_name}(
				product_name TEXT,
				price INTEGER
				)''')

		c.commit()

	except:
		pass

	c.execute(f'DELETE FROM {table_name}')
	# conn.commit()

	for product in scraped_list:
		c.execute(f'INSERT INTO {table_name} VALUES (:product_name, :price)',
				{
				'product_name': product[0],
				'price': product[1]
				})

	conn.commit()
	conn.close()


