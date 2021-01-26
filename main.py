
# Call necessary libraries
from bs4 import BeautifulSoup as bs
import requests
import re

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
    page = requests.get(url)
    # Parse
    html = bs(page.text, 'lxml')
    # To print html source code
    #print(html)
    # Quick test
    test = html.find('h1', class_ = 'hidden menu-title-xs')
    # Replace tilde issue in html
    print(test.text[:15] + 'Ó' + test.text[17:])

    # Print 1 earhquake
    empty = []
    info = ['Fecha: ', 'Magnitud: ', 'Hora: ', 'Latitud: ', 'Longitud: ']

    #print(magnitude)
    quake1 = html.find('tr', class_ = '1days')
    print(quake1.text)
    
    date      =	info[0] + quake1.text[5:16]
    magnitude = info[1] + quake1.text[1:4]
    time 	  = info[2] + quake1.text[27:35]
    # change to negative indexes due the fact that places have different names
    latitute  =	info[3] + quake1.text[71:76] + quake1.text[77]
    longitute = info[4] + quake1.text[80:86] + quake1.text[87]

    #print(newMagnitude)
    #print(list(quake1.text).index("8"))
    print(list(quake1.text))
    #lst = magnitude + list(quake1.text)
    print(''.join(date))
    print(''.join(time))
    print(''.join(magnitude))
    print(''.join(latitute))
    print(''.join(longitute))


    print()
    print('(******************************************************************')
    # Print Multiple earthquakes
    #quakeAll = html.find_all('tr')
    #for last in quakeAll:
    #    print(last.text)







# To allow to use the program as a module
if __name__ == '__main__':
	listEarthquake()

