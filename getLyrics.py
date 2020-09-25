# Nathan Shulkin
# get lyrics and download to file (from genius, page already found)
#
# WANT TO GET TOTAL UNIQUE WORDS FOR ARTIST
#
#
# pip3 install requests
# pip3 install bs4
# pip3 install re
#
# imports
import requests
import bs4
import re
import getPage


# data structure for song
class Music:

    def __init__(self, lyr, lCount, uniq, uCount, uwScore, song, artist, album):
        self.lyr = lyr
        self.lCount = lCount
        self.uniq = uniq
        self.uCount = uCount
        self.uwScore = uwScore
        self.song = song
        self.artist = artist
        self.album = album


# function for lyric parsing
def lyricParse(urlParse, songName, albDict, uniqueList, lyricsAllThe):
    # download url
    print(urlParse)
    req = requests.get(urlParse)
    req.raise_for_status()

    # use url
    soup = bs4.BeautifulSoup(req.text, features='html.parser')

    # find lyrics section
    lyricSearch = str(soup.findAll('div', {'class': 'lyrics'})).replace('<br/>', ' ') \
        .replace('[<div class="lyrics">', '') \
        .replace('<!--sse-->', '') \
        .replace('<p>', '') \
        .replace('</p>', '') \
        .replace('<!--/sse-->', '') \
        .replace('<i>', '') \
        .replace('</i>', '') \
        .replace('</div>]', '') \
        .replace('!', '').replace(',', '').replace('{', '').replace('?', '') \
        .replace('<b>', '').replace('</b>', '') \
        .replace('<em>', '').replace('</em>', '')

    # regular expression to fix links w/ lyrics from genius.com
    reg1 = re.compile(r'(</a>)')
    reg2 = re.compile(r'(<a annotation-fragment="(.*)")')
    reg3 = re.compile(r'{\s*((.*)\'(.*)\': (.*),)+')
    reg4 = re.compile(r'(\'(.*)--(.*)\': (.*))+')
    reg5 = re.compile(r'(\s*}"(.*)-click="">)')
    reg6 = re.compile(r'(\[(.*)\])')
    reg7 = re.compile(r'(\s*}" ng-click="(.*)()" ((.*)-)+)')
    reg8 = re.compile(r'ids="(\d*)">')

    lyricOne = reg1.sub('', lyricSearch)
    lyricTwo = reg2.sub('', lyricOne)
    lyricThree = reg3.sub('', lyricTwo)
    lyricFour = reg4.sub('', lyricThree)
    lyricFive = reg5.sub('\n', lyricFour)
    lyricSix = reg6.sub('', lyricFive)
    lyricSeven = reg7.sub('', lyricSix)
    lyrics = reg8.sub('\n', lyricSeven)

    # print(lyrics)

    unique = []
    for word in lyrics.lower().split():
        # song unique
        if word not in unique:
            unique.append(word)
        # album/total unique
        if word not in uniqueList:
            uniqueList.append(word)
        # album overall total (non unique) for search function
        lyricsAllThe.append(word)

    #
    # find length of song IN PROGRESS, HAVEN'T FIGURED OUT YET
    #

    # get number of words, number of unique words, and UW Score
    lyricCount = len(lyrics.split())
    uniqueCount = len(unique)

    try:
        uwScore = float(uniqueCount / lyricCount)
    except ZeroDivisionError:
        print('\n\n\nzero division error, ' + songName + ' had no lyrics')
        uwScore = 0
        print(lyrics)

    # song data for each song
    songInfo = Music(lyrics, lyricCount, unique, uniqueCount, uwScore, songName.replace('Lyrics', ' '),
                     songArtist.replace('-', ' '), songAlbum.replace('-', ' '))

    # display
    print('\n\n')
    print(songInfo.song + '\nby ' + songInfo.artist)
    print('\n')
    print('Number of words: ' + str(songInfo.lCount))
    print('Number of unique words: ' + str(songInfo.uCount))
    print('Unique Words Score: ' + str(round(songInfo.uwScore, 3)))

    # album dictionary for song scores
    albDict.setdefault(songInfo.song)
    albDict[songInfo.song] = songInfo


# get data from previous programs
if getPage.choice == 2:
    # url = getPage.newAlbum.urlList[0]
    urlList = getPage.newAlbum.urlList
if getPage.choice == 1:
    url = getPage.newSong.url

    # STILL NEED TO FIGURE OUT
    # search function/counter
    #

# set up structures for song name and album info
songTitle = []
albumInfoDict = {}
total = 0
totUnique = []
allTheLyrics = []

if getPage.choice == 2:
    # fill songTitle with song titles
    for title in urlList.keys():
        songTitle.append(title)

# if album
if getPage.choice == 2:
    songArtist = getPage.newAlbum.artist
    songAlbum = getPage.newAlbum.name

    for title in urlList.keys():
        songTitle.append(title)
    i = 0
    for link in urlList.values():
        lyricParse(link, str(songTitle[i]), albumInfoDict, totUnique, allTheLyrics)
        i += 1

# if song
else:
    songArtist = getPage.newSong.artist
    songAlbum = getPage.newSong.albumName
    nameSong = getPage.newSong.name.replace('-', ' ')
    lyricParse(url, nameSong, albumInfoDict, totUnique, allTheLyrics)

# total lyric count
for song in albumInfoDict.values():
    total += song.lCount


print('\n\n\n')
print(total)
print(len(totUnique))

