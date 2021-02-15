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
[X] Display list of earquakes
[] Display intensity chart  (or just show unam scale from parser)
[X] Create CSV file for data
* Send notification via sms/discord/signal/telegram about earthquake
'''

# Call necessary libraries
# Decide which library to use depending in updates from this project
from bs4 import BeautifulSoup as bs
import csv, itertools, pandas, re, requests, sys

# TODO
# Add intensity category (either unam scale or international scale)
# Good comments
# Executable script or leave as a module
# try telegram/whatsapp/signal to receive message


def welcome_printer():
    '''Prints a Welcome Message with options to the end user

    keyword arguments:
    none

    Returns:
    A message with options to enable tobenamedfunction()

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
    days = ['1days', '2days' ,'3days']
    quake_all = len(source.find_all('tr', class_ = days[0]))
    # Variables for three days =================================================
    # Sources to how to create more efficient way for multiple lists
    # https://stackoverflow.com/questions/2402646/python-initializing-multiple-lists-line
    # https://www.geeksforgeeks.org/python-initializing-multiple-lists/
    date_list = []
    time_list = []
    magn_list = []
    latt_list = []
    long_list = []
    prof_list = []
    epic_list = []
    loct_list = []
    degree_symbol = "\u00B0"

    # https://stackoverflow.com/questions/13437251/getting-id-names-with-beautifulsoup/13437437
    # https://stackoverflow.com/questions/2830530/matching-partial-ids-in-beautifulsoup
    # This part extract all ids from website
    #texto = '<span id="foo"></span> <div id="bar"></div>'

    # try using half id name to verify if identiy all similar, Original: True
    # ^mag_\d+
    for tag in source.findAll('td',{'id':re.compile('^mag_1_\d+')}) :
        magn_list.append(tag['id'])

    for tag3 in source.findAll('td',{'id':re.compile('^prof_1_\d+')}) :
        prof_list.append(tag3['id'])

    print('=++++++++++++++++++++++++++++++++++++++++++++++')
    # Print Multiple earthquakes
    for item in range(total_quakes):
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


    print(quake_all) # Prints number of eathquake per days
    # ==========================================================================


def generate_csv(source):
    '''Generates CSV file (to add up to 3 days)

    Keyword Arguments:
    source - Allows the connection and lxml parsing to a website

    Returns:
    csv file with earthquake information

    '''

    days = ['1days', '2days' ,'3days']
    quake_all = len(source.find_all('tr', class_ = days[0]))
    quake_1st = len(source.find_all('tr', class_ = days[0]))
    quake_2nd = len(source.find_all('tr', class_ = days[1]))
    quake_3rd = len(source.find_all('tr', class_ = days[2]))

    # Quick test for each earthquake for three days
    total_quakes = quake_1st + quake_2nd + quake_3rd
    print(f'day1 = {quake_1st}')
    print(f'day2 = {quake_2nd}')
    print(f'day3 = {quake_3rd}')
    print(f'total {total_quakes}')
    # Variables for three days =================================================
    # Sources to how to create more efficient way for multiple lists
    # https://stackoverflow.com/questions/2402646/python-initializing-multiple-lists-line
    # https://www.geeksforgeeks.org/python-initializing-multiple-lists/
    date_list = []
    time_list = []
    magn_list = []
    latt_list = []
    long_list = []
    prof_list = []
    epic_list = []
    loct_list = []

    # https://stackoverflow.com/questions/13437251/getting-id-names-with-beautifulsoup/13437437
    # https://stackoverflow.com/questions/2830530/matching-partial-ids-in-beautifulsoup
    # This part extract all ids from website
    #texto = '<span id="foo"></span> <div id="bar"></div>'

    # try using half id name to verify if identiy all similar, Original: True
    # ^mag_\d+
    day1_list = []
    day2_list = []
    day3_list = []

    for tag in source.findAll('td',{'id':re.compile('^mag_1_\d+')}) :
        magn_list.append(tag['id'])

    for tagi in source.findAll('td',{'id':re.compile('^mag_2_\d+')}) :
        magn_list.append(tagi['id'])

    for tagii in source.findAll('td',{'id':re.compile('^mag_3_\d+')}) :
        magn_list.append(tagii['id'])

    for tag3 in source.findAll('td',{'id':re.compile('^prof_1_\d+')}) :
        prof_list.append(tag3['id'])

    for tag3i in source.findAll('td',{'id':re.compile('^prof_2_\d+')}) :
        prof_list.append(tag3i['id'])

    for tag3ii in source.findAll('td',{'id':re.compile('^prof_3_\d+')}) :
        prof_list.append(tag3ii['id'])

    for tag_day1 in source.findAll('tr',{'id':re.compile('^1day_\d+')}) :
        day1_list.append(tag_day1['id'])

    for tag_day2 in source.findAll('tr',{'id':re.compile('^2day_\d+')}) :
        day2_list.append(tag_day2['id'])

    for tag_day3 in source.findAll('tr',{'id':re.compile('^3day_\d+')}) :
        day3_list.append(tag_day3['id'])


    print('=++++++++++++++++++++++++++++++++++++++++++++++')

    day1 = 1
    day2 = 1
    day3 = 1

    # emulate switch case
    for item in range(total_quakes):
        if item < quake_1st:
            date_list.append('date_1_' + str(day1))
            time_list.append('time_1_' + str(day1))
            loct_list.append('epi_1_' + str(day1))
            latt_list.append('lat_1_' + str(day1))
            long_list.append('lon_1_' + str(day1))
            day1 = day1 + 1
        elif item < (quake_1st + quake_2nd):
            date_list.append('date_2_' + str(day2))
            time_list.append('time_2_' + str(day2))
            loct_list.append('epi_2_' + str(day2))
            latt_list.append('lat_2_' + str(day2))
            long_list.append('lon_2_' + str(day2))
            day2 = day2 + 1
        elif item < (quake_1st + quake_2nd + quake_3rd):
            date_list.append('date_3_' + str(day3))
            time_list.append('time_3_' + str(day3))
            loct_list.append('epi_3_' + str(day3))
            latt_list.append('lat_3_' + str(day3))
            long_list.append('lon_3_' + str(day3))
            day3 = day3 + 1

    #print(date_list)
    # Test with pandas =========================================================

    with open('test2.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Hora", "Magnitud", "Latitud", "Longitud",
         "Lugar", "Profundidad"])


        for i in range(total_quakes):
            magnitudes = source.find(id=magn_list[i]).text
            profundidades = source.find(id=prof_list[i]).text
            dates = source.find(id=date_list[i]).text
            times = source.find(id=time_list[i]).text
            locations = source.find(id=loct_list[i]).text
            latitudes = source.find(id=latt_list[i]).text
            longitudes = source.find(id=long_list[i]).text
            writer.writerow([dates, times, magnitudes, latitudes, longitudes,
             locations, profundidades])

    # ==========================================================================


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


def old_code():
    ''' To hold previous code used

    Keyword Arguments:
    none

    Returns:
    none
    '''
    #for last in quakeAll:
    #	dateAll = html.findAll(id='epi_1_')
    #	print(dateAll)
    #print(last.text)
    #print(dateAll.text)
    '''
    # OLD WAY ##################################################################
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

    # Print Multiple earthquakes ###############################################
    #quakeAll = html.find_all('tr')
    #for last in quakeAll:
    #    print(last.text)
    # To allow single connections ##############################################
    ##url = 'http://www.ssn.unam.mx/sismicidad/ultimos/'
    ##info = requests.get(url).text
    # Read website into code (parse)
    ##source = bs(info, 'lxml')
    ###########################################################################
    # Note to myself, apparently around 23:30 MST class 1days dissappears
    # Try to add like a time function to change 1days to 2days in the future
    #quake1 = html.find('tr', class_ = '1days') #1days
    #print(quake1.text)
    # Add intesity marker green: weak, orange: medium, red: intense
    #last_earthquake(html)
    #show_list(html)
    ############################################################################
    ''' This part works already
    # Print Multiple earthquakes to csv file
    for item in range(quake_1st):
        day1 = day1 + 1
        date_list.append('date_1_' + str(day1))
        #time_list.append('time_1_' + str(day1))
        #loct_list.append('epi_1_' + str(day1))
        #latt_list.append('lat_1_' + str(day1))
        #long_list.append('lon_1_' + str(day1))

    for item2 in range(quake_2nd):
        day2 = day2 + 1
        date_list.append('date_2_' + str(day2))

    for item3 in range(quake_3rd):
        day3 = day3 + 1
        date_list.append('date_3_' + str(day3))

    print('date_list ' + str(len(date_list)))
    '''


# To allow to use the program as a module ======================================
if __name__ == '__main__':
    main()
