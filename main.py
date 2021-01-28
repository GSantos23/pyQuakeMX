'''
pyQuakeMX

This little program allow you to obtain earquake information in Mexico
Using BeautifulSoup as a webscrapping library to obtain unam data

Implementations 

[X[] = Done
[~]  = Half way
[ ]  = In progress
*    = To try first 

[] Display last earthquake
[] Display list of earquakes (around 3 days)
[] Display intensity chart  (or just show unam scale from parser)
* Send notification via sms/discord/signal/telegram about earthquake in fav zone
* Fav Zone will be a file where you put preferred location
'''

# Call necessary libraries
from bs4 import BeautifulSoup as bs
import requests
import re


# TODO
# Function that return/ask argumentrs/parameter into another functions
# Fix list for multiple earthquakes
# Delete unwanted code
# Language function
# Add intensity category (either unam scale or international scale)
# Search by State function
# Pretty rpinting, fstring
# Good comments
# executable script or leave as a module

def welcomePrinter():
    '''
    Prints a Welcome Message with options to the user

    Returns:
    A message with options to enable tobenamedfunction()

    '''
    print('*'*45)
    print(''' Welcome to pyQuakeMX
        Please Select one the following options:
        1) Display last earhquake
        2) Display list of earthquakes
        3) Type State Abbreviations
        4) Exit
            ''')
    print('*'*45)

def listEarthquake():
    welcomePrinter()
    url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
    page = requests.get(url).text

    # Parse
    html = bs(page, 'lxml') # was lxml
    # To print html source code
    #print(html)
    # Quick test
    test = html.find('h1', class_ = 'hidden menu-title-xs')
    # Replace tilde issue in html
    print(test.text[:15] + 'Ó' + test.text[17:])

    # Print 1 earhquake
    info = ['Fecha: ', 'Magnitud: ', 'Hora: ', 'Latitud: ', 'Longitud: ', 'Profundidad: ']

    # Note to myself, apparently around 23:30 MST class 1days dissappears
    # Try to add like a time function to change 1days to 2days in the future
    quake1 = html.find('tr', class_ = '1days') #1days
    print(quake1.text)
    # Prints info using id= instead of string concatenation
    # Add intesity marker (look for usgs term) green: weak, orange: medium, red: intense
    print('Último Sismo =====================================================')
    date     = html.find(id='date_1_1').text
    time	 = html.find(id='time_1_1').text
    magnitud = html.find(id='mag_1_1').text
    latitud  = html.find(id='lat_1_1').text
    longitud = html.find(id='lon_1_1').text
    depth	 = html.find(id='prof_1_1').text
    # remeber depende de la pagian si usa epi_1,2 o 3
    location = html.find(id='epi_1_1').text
    
    print('Fecha: ' + date)
    print('Hora: ' + time)
    print("Magnitud: " +  magnitud)
    print("Epicentro --")
    print("Localización: " + location)
    #degree Symbol = u/'00BO'
    print("Latitud, Longitud: " + latitud + "\u00B0 , " + longitud + "\u00B0")

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







# To allow to use the program as a module
if __name__ == '__main__':
	listEarthquake()

