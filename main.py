'''
pyQuakeMX ======================================================================

This little program allow you to obtain earquake information in Mexico
Using BeautifulSoup as a webscrapping library to obtain unam data

================================================================================

Implementations

[X 	= Done
[~] = Half way
[&] = In progress
[]	= Not implemented yet

[X] Display last earthquake
[X] Display list of earquakes
[X] Create CSV file for data
[] Send notification via sms/discord/signal/telegram about earthquake
'''

# Call necessary libraries
from bs4 import BeautifulSoup as bs
import csv, re, requests, sys

# TODO
# try telegram/whatsapp/signal to receive message


def welcome_printer():
    '''Prints a Welcome Message with options to the end user

    Keyword arguments:
    none

    Returns:
    A message with options to end user

    '''

    print('*'*45)
    print(''' pyQuakeMX
    Selecciona una de las siguientes opciones:
    a) Mostrar ultimo sismo
    b) Mostrar lista de sismos
    c) Generar archivo .csv
    d) Exit
            ''')
    print('*'*45)

#for tag in source.findAll('td',{'id':re.compile('^mag_\d+')}) :
#	magn_list_csv.append(tag['id'])
# param1 = class
# param2 = id
# param3 = regex
# 
def regex_extract(source, tagName, attribute, regex):
	''' Use regex to extract specific html tags and ids
	
	Keyword arguments:
	source  	- Allows the connection and lxml parsing to a website
	tagName 	- HTML tag <X class>  to search
	attribute	- HTML attribute to search
	regex 		- Regex syntax to search

	Returns:
	A list with html tags
	'''
	regex_list = []

	for x in source.findAll(tagName, {attribute:re.compile(regex)}):
		regex_list.append(x[attribute])

	return regex_list


def last_earthquake(source):
    ''' Displays last eathquake information

    Keyword arguments:
    source - Allows the connection and lxml parsing to a website

    Returns:
    date
    time
    magnitute
    coordinates
    depth
    location
    '''

    print('Último Sismo ======================================================')
    date     = source.find(id='date_1_1').text
    time	 = source.find(id='time_1_1').text
    magnitud = source.find(id='mag_1_1').text
    latitud  = source.find(id='lat_1_1').text
    longitud = source.find(id='lon_1_1').text
    depth	 = source.find(id='prof_1_1').text
    location = source.find(id='epi_1_1').text

    print(f'Fecha: {date}')
    print(f'Hora: {time}')
    print(f'Magnitud: {magnitud}')
    print('Epicentro --')
    degree_symbol = "\u00B0"
    print(f'Latitud: {latitud}{degree_symbol}')
    print(f'Longitud: {longitud}{degree_symbol}')
    print(f'Localización: {location} ')
    print(f'Profundidad {depth}')
    print('===================================================================')


def show_list(source):
    '''Displays list of today earthquakes

    Keyword Arguments:
    source - Allows the connection and lxml parsing to a website

    Returns:
    date
    time
    magnitude
    coordinates
    depth
    location
    '''

    print('*******************************************************************')
    days = ['1days']
    quake_all = len(source.find_all('tr', class_ = days[0]))

    # Lists to hold earthquakes information
    date_list = []
    time_list = []
    latt_list = []
    long_list = []
    epic_list = []
    loct_list = []
    degree_symbol = "\u00B0"

    # If you pass in a regular expression object, Beautiful Soup will filter 
    # against that regular expression using its search() method. 
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#a-regular-expression
    mag_regex = '^mag_1_\d+'
    prf_regex = '^prof_1_\d+'

    # Lists that contain regex extraction
    magn_list = regex_extract(source,'td', 'id', mag_regex)
    prof_list = regex_extract(source,'td', 'id', prf_regex)

    #for tag in source.findAll('td',{'id':re.compile('^mag_1_\d+')}) :
     #   magn_list.append(tag['id'])

    #for tag3 in source.findAll('td',{'id':re.compile('^prof_1_\d+')}) :
    #    prof_list.append(tag3['id'])

    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    # Print Multiple earthquakes
    for item in range(quake_all):
        x = item + 1
        date_list.append('date_1_' + str(x))
        time_list.append('time_1_' + str(x))
        loct_list.append('epi_1_' + str(x))
        latt_list.append('lat_1_' + str(x))
        long_list.append('lon_1_' + str(x))


    for i in range(quake_all):
        magnitudes = source.find(id=magn_list[i]).text
        profundidades = source.find(id=prof_list[i]).text
        dates = source.find(id=date_list[i]).text
        times = source.find(id=time_list[i]).text
        locations = source.find(id=loct_list[i]).text
        latitudes = source.find(id=latt_list[i]).text
        longitudes = source.find(id=long_list[i]).text
        print(f'Fecha: {dates}')
        print(f'Hora: {times}')
        print(f'Magnitud: {magnitudes}')
        print('Epicentro --')
        print(f'Latitud: {latitudes}{degree_symbol}')
        print(f'Longitud: {longitudes}{degree_symbol}')
        print(f'Profundidad: {profundidades}')
        print(f'Localización: {locations}')
        print('=========================')


    #print(quake_all) # Prints number of eathquake today


def generate_csv(source):
    '''Generates CSV file (to add up to 3 days)

    Keyword Arguments:
    source - Allows the connection and lxml parsing to a website

    Returns:
    csv file with earthquake information

    '''

    days = ['1days', '2days' ,'3days']
    quake_1st = len(source.find_all('tr', class_ = days[0]))
    quake_2nd = len(source.find_all('tr', class_ = days[1]))
    quake_3rd = len(source.find_all('tr', class_ = days[2]))

    # Quick test for each earthquake for three days
    total_quakes = quake_1st + quake_2nd + quake_3rd
    #print(f'day1 = {quake_1st}')
    #print(f'day2 = {quake_2nd}')
    #print(f'day3 = {quake_3rd}')
    #print(f'total {total_quakes}')
    # Variables for three days =================================================
    date_list_csv = []
    time_list_csv = []
    latt_list_csv = []
    long_list_csv = []
    epic_list_csv = []
    loct_list_csv = []

    # If you pass in a regular expression object, Beautiful Soup will filter 
    # against that regular expression using its search() method. 
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/#a-regular-expression

    # Lists that contain regex extraction
    magn_list_csv = regex_extract(source,'td', 'id', '^mag_\d+')
    prof_list_csv = regex_extract(source,'td', 'id', '^prof_\d+')

    # Remeber why I implement this part =======================================
    #for tag_day1 in source.findAll('tr',{'id':re.compile('^1day_\d+')}) :
    #    day1_list.append(tag_day1['id'])

    #for tag_day2 in source.findAll('tr',{'id':re.compile('^2day_\d+')}) :
    #    day2_list.append(tag_day2['id'])

    #for tag_day3 in source.findAll('tr',{'id':re.compile('^3day_\d+')}) :
    #    day3_list.append(tag_day3['id'])

    #day1_list = regex_extract(source,'td', 'id', '^1day_\d+')
    #day2_list = regex_extract(source,'td', 'id', '^2day_\d+')
    #day3_list = regex_extract(source,'td', 'id', '^3day_\d+')
    ##==========================================================================


    print('=++++++++++++++++++++++++++++++++++++++++++++++')

    day1 = 1
    day2 = 1
    day3 = 1

    # emulate switch case
    for item in range(total_quakes):
        if item < quake_1st:
            date_list_csv.append('date_1_' + str(day1))
            time_list_csv.append('time_1_' + str(day1))
            loct_list_csv.append('epi_1_' + str(day1))
            latt_list_csv.append('lat_1_' + str(day1))
            long_list_csv.append('lon_1_' + str(day1))
            day1 = day1 + 1
        elif item < (quake_1st + quake_2nd):
            date_list_csv.append('date_2_' + str(day2))
            time_list_csv.append('time_2_' + str(day2))
            loct_list_csv.append('epi_2_' + str(day2))
            latt_list_csv.append('lat_2_' + str(day2))
            long_list_csv.append('lon_2_' + str(day2))
            day2 = day2 + 1
        elif item < (quake_1st + quake_2nd + quake_3rd):
            date_list_csv.append('date_3_' + str(day3))
            time_list_csv.append('time_3_' + str(day3))
            loct_list_csv.append('epi_3_' + str(day3))
            latt_list_csv.append('lat_3_' + str(day3))
            long_list_csv.append('lon_3_' + str(day3))
            day3 = day3 + 1

    # Pandas only if >1K Rows
    # https://stackoverflow.com/questions/62139040/python-csv-module-vs-pandas
    # Use writer object and writerow() method to create csv file
    with open('earthquakeList.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Hora", "Magnitud", "Latitud", "Longitud",
         "Lugar", "Profundidad"])

        for i in range(total_quakes):
            magnitudes = source.find(id=magn_list_csv[i]).text
            profundidades = source.find(id=prof_list_csv[i]).text
            dates = source.find(id=date_list_csv[i]).text
            times = source.find(id=time_list_csv[i]).text
            locations = source.find(id=loct_list_csv[i]).text
            latitudes = source.find(id=latt_list_csv[i]).text
            longitudes = source.find(id=long_list_csv[i]).text
            writer.writerow([dates, times, magnitudes, latitudes, longitudes,
             locations, profundidades])


def main():
    '''Main function

    Keyword Arguments:
        none

    Returns:
        * Information related to last earthquake in Mexico
    '''
    print('*******************************************************************')
    url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
    unam = requests.get(url).text
    source = bs(unam, 'lxml')
    days = ['1days', '2days' ,'3days']
    quake_all = len(source.find_all('tr', class_ = days[0]))

    welcome_printer()
    url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
    page = requests.get(url).text

    # Parse code
    html = bs(page, 'lxml') # was lxml

    # To print html source code
    #print(html)

    userInput = input('Teclea opcion: ')

    # Print title of website
    test = html.find('h1', class_ = 'hidden menu-title-xs')

    # Replace tilde issue in html
    print(test.text[:15] + 'Ó' + test.text[17:])

    # Simple switch handler
    while True:
        if (userInput == 'a'):
            last_earthquake(html)
        elif (userInput == 'b'):
            show_list(html)
        elif (userInput == 'c'):
            print('Generando archivo ......')
            generate_csv(html)
        elif (userInput == 'd'):
            sys.exit("Hasta la proxima")
        else:
            sys.exit("Error!. Corra nuevamente el programa usando opciones validas")

        welcome_printer()
        userInput = input('Teclea opcion: ')

    print()
    print('******************************************************************')


# To allow to use the program as a module ======================================
if __name__ == '__main__':
    main()
