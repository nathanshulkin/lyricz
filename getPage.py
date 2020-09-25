# Nathan Shulkin
# ask for song name and artist and then search google for genius lyrics, click on/get url
#
#
# pip3 install webdriver
# brew install selenium
# pip3 install mysql-connector-python
#
#
# imports
from selenium import webdriver
import time
import re

# structures
class Album:

    def __init__(self, name, artist, urlList, trackList, timeLength, albumLength):
        self.name = name
        self.artist = artist
        self.urlList = urlList
        self.trackList = trackList
        self.timeLength = timeLength
        self.albumLength = albumLength


class Song:

    def __init__(self, name, artist, albumName, url, timeLength, albumLength):
        self.name = name
        self.artist = artist
        self.albumName = albumName
        self.url = url
        self.timeLength = timeLength
        self.albumLength = albumLength


# methods
def getAlbum(songAlbum, songArtist, timeLength, url, urlList, trackList):
    # ask person
    print('\n\nWhat is the name of the album?')
    songAlbum = str(input().replace(' ', '-'))

    print('\nand the artist?')
    songArtist = str(input().replace(' ', '-'))

    print('\nHow long is the album? (in seconds)')
    timeLength = int(input())

    # search part

    # webdriver/open internet
    browser = webdriver.Firefox()

    # google thing
    browser.get('https://google.com/search?q=' + songArtist + ' ' + songAlbum + ' album tracklist genius.com'
                + '&start=')

    # find and click on first/specific google link
    url = browser.find_element_by_xpath('//a[starts-with(@href, "https://genius.com")]')

    # if url exists/was found
    if url:
        url.click()

    else:
        print('sorry, couldn\'t properly execute the designed function')

    # do whole album instead of one song

    time.sleep(5)
    print('\n\nComputering...')
    urlList = {}
    trackList = []

    # WORKING
    url = browser.find_elements_by_class_name('chart_row-content')

    # tracklist counter
    i = 0
    for link in url:

        # if song too long
        if len(link.text) > 101:
            # take out features of parenthesis
            trimReg1 = re.compile(r'\((.*)\) ')
            trimReg2 = re.compile(r'[f:F][t:T]\.?(.*)')
            shorter = trimReg1.sub('', link.text)
            shorter = trimReg2.sub('', shorter)
            trackList.append(shorter)
        else:
            trackList.append(link.text)
        i += 1

    print('\n\nComputering...\n')

    # length of album
    albumLength = len(trackList)

    # iterate through album
    for item in trackList:

        tang = 0

        # google thing
        browser.get('https://google.com/search?q=' + songArtist + ' genius.com ' + item
                    + '&start=')

        # find and click on first/specific google link, for some reason tangerine by glass animals doesn't work
        if item.lower() == 'tangerine lyrics':
            print('tangerine')
            url = browser.get('https://genius.com/Glass-animals-tangerine-lyrics')
            print(url)
            print(browser.current_url)
            tang = 1
        else:
            print('getting ' + item)
            url = browser.find_element_by_xpath('//a[starts-with(@href, "https://genius.com")]')

        # if url exists/was found
        if url:
            time.sleep(2)
            if tang != 1:
                url.click()
            urlList.setdefault(item)
            urlList[item] = browser.current_url

        else:
            print('sorry, couldn\'t properly execute the designed function')

    return Album(songAlbum, songArtist, urlList, trackList, timeLength, albumLength)


def getSong(songName, songArtist, songAlbum, url, timeLength, albumLength):
    albumLength = 1
    print('\n\nWhat is the name of the song?')
    songName = str(input().replace(' ', '-'))

    print('\nand the artist?')
    songArtist = str(input().replace(' ', '-'))

    print('\nand the album? (just leave blank if you don\'t know)')
    songAlbum = str(input().replace(' ', '-').replace('\\n', ''))

    print('\nwhat is the length of the song? (in seconds)')
    timeLength = int(input())

    # search part

    # webdriver/open internet
    browser = webdriver.Firefox()

    # google thing
    browser.get('https://google.com/search?q=' + songArtist + ' ' + songName + ' song lyrics genius.com'
                + '&start=')

    # find and click on first/specific google link
    url = browser.find_element_by_xpath('//a[starts-with(@href, "https://genius.com")]')

    # if url exists/was found
    if url:
        url.click()

    else:
        print('sorry, couldn\'t properly execute the designed function')

    url = browser.current_url
    # create new song
    return Song(songName, songArtist, songAlbum, url, timeLength, albumLength)



# variables needed
songName = ''
songArtist = ''
songAlbum = ''
url = ''
timeLength = 0
albumLength = 0
urlList = {}
trackList = []


# ask person
print('\nPlease do everything lowercase.\n\n')

print('Would you like to do: \n1. Song\n2. Album')
choice = 0;

try:
    choice = int(input())
except ValueError:
    print('\nSorry, please pick either 1 or 2.')
    choice = int(input())


# error case
while choice != 1 and choice != 2:
    print('Sorry, please select a valid input and try again.')
    choice = int(input())

# if album
if choice == 2:

    newAlbum = getAlbum(songAlbum, songArtist, timeLength, url, urlList, trackList)

# if song
else:

    newSong = getSong(songName, songArtist, songAlbum, url, timeLength, albumLength)
