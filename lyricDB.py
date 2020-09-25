# Nathan Shulkin
# create database and add song info (from getLyrics.py) to database
#
#
# pip3 install mysql-connector-python
#

import getLyrics
import getPage
import mysql.connector


# get password
print('what is the password?')
psswd = str(input())

# create DB
# DB MUST EXIST/BE CREATED IN MYSQL (USE TERMINAL) AND CREATE TABLE IN DB
lyricDB = mysql.connector.connect(
    host="192.168.0.6",  # IP address / server address
    user="root",
    password= psswd,  # computer user password
    database="lyricDB"
)

# initialize DB
lyricCursor = lyricDB.cursor()

print('what database would you like to use?')
dbChoice = str(input())

dbCheck = 0
while dbCheck == 0:
    try:
        # initialize DB
        check = "select * from " + dbChoice
        lyricCursor.execute(check)
        checkords = lyricCursor.fetchall()
        dbCheck = 1
    except:
        print('\nsorry that was not one of the databases. Try again.')
        dbChoice = str(input())

# if album
if getPage.choice == 2:
    timeLength = getPage.newAlbum.timeLength
    albumLength = getPage.newAlbum.albumLength
else:
    timeLength = getPage.newSong.timeLength
    albumLength = 1

if getLyrics.songAlbum in str(checkords):
    print('this album is already in the ' + dbChoice + ' database, not added.')
else:
    # add to DB
    sql = 'INSERT INTO ' + dbChoice + '(artist, album, lyrCount, uCount, uwScore, time, numbSongs)' \
                                          'VAlUES (%s, %s, %s, %s, %s, %s, %s)'
    val = (getLyrics.songArtist, getLyrics.songAlbum,
           getLyrics.total, len(getLyrics.totUnique),
           (len(getLyrics.totUnique)/getLyrics.total), timeLength, albumLength)
    lyricCursor.execute(sql, val)
    print(getLyrics.songAlbum + ' added to ' + dbChoice)

# get songnames from database for check
lyricCursor.execute('SELECT songName FROM lyrics')
checkDB = lyricCursor.fetchall()

print('\n\n\n')

# add info to song database
for song in getLyrics.albumInfoDict.keys():
    if song in str(checkDB):
        print(song + ' is already in database, not added.')
    else:
        # add to DB
        sql = 'INSERT INTO lyrics (artist, songName, album, lyrCount, uniqCount, uwScore)' \
                'VALUES (%s, %s, %s, %s, %s, %s)'
        val = (getLyrics.albumInfoDict[song].artist, getLyrics.albumInfoDict[song].song,
               getLyrics.albumInfoDict[song].album, getLyrics.albumInfoDict[song].lCount,
               getLyrics.albumInfoDict[song].uCount, getLyrics.albumInfoDict[song].uwScore)

        lyricCursor.execute(sql, val)
        print(song + ' added to database.')


# total words, unique words, number of songs for artist database

# get artist name to check if already in database
lyricCursor.execute('SELECT artist FROM artistTot')
checkDB = lyricCursor.fetchall()

print('\n\n\n')

# if album not song
artist = str(getLyrics.songArtist).replace('-', ' ')

if artist in str(checkDB):
    print(artist + ' is already in the artist database, would you like to continue?'
                   '\n1. yes \n2. no')
    choice = int(input())

    while choice != 1 and choice != 2:
        print('sorry, please select a valid choice.')
        choice = int(input())

    if choice == 1:

        # get lyric total from db
        sql = "SELECT lyricTOT FROM artistTOT WHERE artist like \"" + str(artist) + "\""
        lyricCursor.execute(sql)
        result = lyricCursor.fetchall()
        # update lyric total
        lyrTOT = (int(result[0][0]) + getLyrics.total)

        print(str(int(result[0][0])) + ' + ' + str(getLyrics.total) + ' = ' + str(lyrTOT))

        # get unique total from db
        sql = "SELECT uniqTOT FROM artistTOT WHERE artist like \"" + str(artist) + "\""
        lyricCursor.execute(sql)
        result = lyricCursor.fetchall()
        # update unique total
        uniqTOT = (int(result[0][0]) + len(getLyrics.totUnique))

        print(str(int(result[0][0])) + ' + ' + str(len(getLyrics.totUnique)) + ' = ' + str(uniqTOT))

        # get number of songs from db
        sql = "SELECT numbSongs FROM artistTOT WHERE artist like \"" + str(artist) + "\""
        lyricCursor.execute(sql)
        result = lyricCursor.fetchall()
        songNumb = (int(result[0][0]) + len(getLyrics.albumInfoDict))

        print(str(int(result[0][0])) + ' + ' + str(len(getLyrics.albumInfoDict)) + ' = ' + str(songNumb))

        # update database
        sql = "UPDATE artistTot set lyricTOT=\"" + str(lyrTOT) + "\" WHERE artist LIKE \"" + str(artist) + "\""
        lyricCursor.execute(sql)

        sql = "UPDATE artistTot set uniqTOT=\"" + str(uniqTOT) + "\" WHERE artist LIKE \"" + str(artist) + "\""
        lyricCursor.execute(sql)

        sql = "UPDATE artistTot set numbSongs=\"" + str(songNumb) + "\" WHERE artist LIKE \"" + str(artist) + "\""
        lyricCursor.execute(sql)

        print(artist + ' lyric totals added to database')

    else:
        print('thank you, all done.')

else:
    val = artist

    # add artist to database
    sql = 'INSERT INTO artistTot (artist, lyricTOT, uniqTOT, numbSongs)' \
        'VALUES (%s, %s, %s, %s)'

    # if album
    if getPage.choice == 2:
        val = (artist, getLyrics.total, len(getLyrics.totUnique), getPage.newAlbum.albumLength)

    # if song
    else:
        val = (artist, getLyrics.total, len(getLyrics.totUnique), getPage.albumLength == 1)

    lyricCursor.execute(sql, val)
    print(artist + ' lyric totals added to database')


# ALWAYS SAVE CHANGES TO DB
lyricDB.commit()
