'''
pyQuakeMX ======================================================================

This little program allow you to obtain earquake information in Mexico
Using BeautifulSoup as a webscrapping library to obtain unam data

================================================================================

Implementations

[X[] = Done
[~]  = Half way
[&]  = In progress
*    = To try first

[X] Display last earthquake
[~] Display list of earquakes (around 3 days)
[] Display intensity chart  (or just show unam scale from parser)
[] Create CSV file for data
* Send notification via sms/discord/signal/telegram about earthquake in fav zone
* Fav Zone will be a file where you put preferred location
'''

# Call necessary libraries
from bs4 import BeautifulSoup as bs
import requests
import re


# TODO
# create a  dummy method for old code, ie. oldForm() some code in here pass
# Check PEP-8 multiline comments format
# define good variable names
# add url as paramter in the function to avoid multiple connections
# reasearch about fstring format available, advantages, disadvantages
# Add switch case/if-else to handle input of user to select between options
# Add intensity category (either unam scale or international scale)
# Good comments
# Executable script or leave as a module
# Add functionality to create csv file
# Add funcitonality to allow showList() to select day or days to display 
# try in ubuntu/debian/windows after installing components
# try telegram/whatsapp/signal to receive message
# 

def welcomePrinter():
    '''
    Prints a Welcome Message with options to the user

    Returns:
    A message with options to enable tobenamedfunction()

    '''
    print('*'*45)
    print(''' pyQuakeMX
        Selecciona una de las siguientes opciones:
        1) Mostrar ultimo sismo
        2) Mostrar lista de sismos
        3) Exit
            ''')
    print('*'*45)

def lastEarhquake():
    '''
    Displays last eathquake information
	No arguments
	Returns:
		date
		time
		magnitute
		coordinates
		depth
		location
    '''

    # Website of UNAM for earthquakes
    url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
    info = requests.get(url).text
    # Read website into code (parse)
    source = bs(info, 'lxml')
    print('Último Sismo ======================================================')
    date     = source.find(id='date_1_1').text
    time	 = source.find(id='time_1_1').text
    magnitud = source.find(id='mag_1_1').text
    latitud  = source.find(id='lat_1_1').text
    longitud = source.find(id='lon_1_1').text
    depth	 = source.find(id='prof_1_1').text
    location = source.find(id='epi_1_1').text

    print('Fecha: ' + date)
    print('Hora: ' + time)
    print('Magnitud: ' +  magnitud)
    print('Epicentro --')
    #degree Symbol = 'u00BO'
    print('Latitud: ' + latitud + '\u00B0')
    print('Longitud: ' + longitud + '\u00B0')
    print('Localización: ' + location)
    print('Profundidad ' + depth)
    print('===================================================================')

def showList():
	'''
	Displays list of earquakes until now(Today)
	No arguments
	Returns:
		date
		time
		magnitude
		coordinates
		depth
		location
	'''
	print('*******************************************************************')
	url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
	unam = requests.get(url).text
	pool = bs(unam, 'lxml')
	result = []
	rslPrf = []
	days = ['1days', '2days' ,'3days']
	quakeAll = len(pool.find_all('tr', class_ = days[0]))
	# Variables for three days =================================================
	# Sources to how to create more efficient way for multiple lists
	# https://stackoverflow.com/questions/2402646/python-initializing-multiple-lists-line
	# https://www.geeksforgeeks.org/python-initializing-multiple-lists/
	dateLst = []
	timeLst = []
	magnLst = []
	lattLst = []
	longLst = []
	profLst = []
	epicLst = []
	loctLst = []

	# https://stackoverflow.com/questions/13437251/getting-id-names-with-beautifulsoup/13437437
	# https://stackoverflow.com/questions/2830530/matching-partial-ids-in-beautifulsoup
	# This part extract all ids from website
	#texto = '<span id="foo"></span> <div id="bar"></div>'

	# try using half id name to verify if identiy all similar, Original: True
	# ^mag_\d+
	for tag in pool.findAll('td',{'id':re.compile('^mag_1_\d+')}) :
	    result.append(tag['id'])

	for tag3 in pool.findAll('td',{'id':re.compile('^prof_1_\d+')}) :
	    rslPrf.append(tag3['id'])

	print('=++++++++++++++++++++++++++++++++++++++++++++++')
	# Print Multiple earthquakes
	for item in range(quakeAll):
		x = item + 1
		dateLst.append('date_1_' + str(x))
		timeLst.append('time_1_' + str(x))
		loctLst.append('epi_1_' + str(x))
		lattLst.append('lat_1_' + str(x))
		longLst.append('lon_1_' + str(x))

	# Test witth pretty table
	#
	for i in range(quakeAll):
		magnitudes = pool.find(id=result[i]).text
		profundidades = pool.find(id=rslPrf[i]).text
		dates = pool.find(id=dateLst[i]).text
		times = pool.find(id=timeLst[i]).text
		locations = pool.find(id=loctLst[i]).text
		latitudes = pool.find(id=lattLst[i]).text
		longitudes = pool.find(id=longLst[i]).text
		print('Fecha: ' + dates)
		print('Hora: ' + times)
		print("Magnitud: " +  magnitudes)
		print("Epicentro --")
		print('Latitud: ' + latitudes + '\u00B0')
		print('Longitud: ' + longitudes + '\u00B0')
		print("Profundidad: " +  profundidades)
		print('Localización: ' + locations)
		print('=========================')


	print(quakeAll) # Prints number of eathquake per days
	# ==========================================================================	


def listEarthquake():

    welcomePrinter()
    url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
    page = requests.get(url).text

    # Parse code
    html = bs(page, 'lxml') # was lxml
    # To print html source code
    #print(html)

    # Print title of website
    test = html.find('h1', class_ = 'hidden menu-title-xs')

    # Replace tilde issue in html
    print(test.text[:15] + 'Ó' + test.text[17:])

    # Note to myself, apparently around 23:30 MST class 1days dissappears
    # Try to add like a time function to change 1days to 2days in the future
    #quake1 = html.find('tr', class_ = '1days') #1days
    #print(quake1.text)


    # Add intesity marker (look for usgs term) green: weak, orange: medium, red: intense
    # For the moment display just last day earquake list
    # Idea: Use regex to call id for multiple days, depending of user input
    
    lastEarhquake()
    showList()

    

    #for last in quakeAll:
    #	dateAll = html.findAll(id='epi_1_')
    #	print(dateAll)
        #print(last.text)
        #print(dateAll.text)
    '''
    # OLD WAY
    date      =	info[0] + quake1.text[5:16]
    magnitude = info[1] + quake1.text[1:4]
    time 	  = info[2] + quake1.text[27:35]
    depth     = info[5] + quake1.text[-7:-1]
    # change to negative indexes due the fact that places have different names
    latitute  =	info[3] + quake1.text[71:76] + quake1.text[77]
    longitute = info[4] + quake1.text[80:86] + quake1.text[87]


    #print(newMagnitude)
    print(len(quake1.text))
    #print(list(quake1.text).index("8"))
    print(list(quake1.text))
    #lst = magnitude + list(quake1.text)
    print(''.join(date))
    print(''.join(time))
    print(''.join(magnitude))
    print(''.join(latitute))
    print(''.join(longitute))

    print(''.join(depth))
    '''


    print()
    print('******************************************************************')
    # Print Multiple earthquakes
    #quakeAll = html.find_all('tr')
    #for last in quakeAll:
    #    print(last.text)




# To allow to use the program as a module ======================================
if __name__ == '__main__':
	listEarthquake()

