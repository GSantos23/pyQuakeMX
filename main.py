
# Call necessary libraries
from bs4 import BeautifulSoup as bs
import requests
import re

print('Welcome to pyUSGS...')

def listEarthquake():
	url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
	page = requests.get(url)
	# Parse
	html = bs(page.text, 'lxml')
	# To print html source code
	#print(html)
	
	# Quick test
	test = html.find('h1', class_ = 'hidden menu-title-xs')
	print(test.text)

	# Print 1 earhquake
	quake1 = html.find('tr', class_ = '1days')
	print(quake1.text)
	print()
	print('(******************************************************************')
	# Print Multiple earthquakes
	quakeAll = html.find_all('tr')
	for last in quakeAll:
		print(last.text)







# To allow to use the program as a module
if __name__ == '__main__':
	listEarthquake()

