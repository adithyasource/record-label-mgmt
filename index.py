import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import Toplevel

import sqlite3
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Space Grotesk"
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.cm as cm

from customtkinter import set_appearance_mode
from customtkinter import CTkCheckBox
from customtkinter import CTkFont

from googleapiclient.discovery import build
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import configparser
import webbrowser
import socket
import io
import shutil
import os
import sys





def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)
# defines a restart function, to be used later

window = tk.Tk()
window.title('MIMIC Internal Mgmt')
windowWidth = 985
windowHeight = 450
# creates the window for the app

def onClosing():
    global windowWidth, windowHeight
    windowWidth = window.winfo_width()
    windowHeight = window.winfo_height()
    with open("windowSize.txt", "w") as f:
        f.write(str(windowWidth) + "\n")
        f.write(str(windowHeight) + "\n")
    window.destroy()
window.protocol("WM_DELETE_WINDOW", onClosing)
# when called upon, it checks the size of the window and then stores it to a textfile windowSize.txt


try:
    with open("windowSize.txt", "r") as f:
        windowWidth = int(f.readline())
        windowHeight = int(f.readline())
except FileNotFoundError:
    pass
# runs at startup and reads the textfile windowSize.txt and sets the size of the window to it


window.geometry(f"{windowWidth}x{windowHeight}")
window.resizable(False, True)
window.iconbitmap('mimic.ico')
window.configure(bg='#FFFFFF')
window.pack_propagate(False)
set_appearance_mode('light')
# configuring the window for the app

frame = tk.Frame(window, bg='#FFFFFF')
frame2 = tk.Frame(window, bg='#FFFFFF')
tempFrameForEntry = tk.Frame(window, bg='#FFFFFF')
frameForTracking = tk.Frame(window, bg='#FFFFFF')
frameForAnalytics = tk.Frame(window, bg='#FFFFFF')
frameForError = tk.Frame(window, bg='#FFFFFF')
frameForErrorNoAnalytics = tk.Frame(window, bg='#FFFFFF')
# creating the different frames / pages that the app will use through its runtime


songLocation = ''


try:
    socket.create_connection(('8.8.8.8', 53))
    isInternetConnected = True
except OSError:
    isInternetConnected = False
# check if pc is connected to the internet by pinging google's dns and returns bool value


if isInternetConnected == True:
    for page in (frame, frame2, tempFrameForEntry, frameForTracking, frameForAnalytics, frameForErrorNoAnalytics):
        page.grid(row=0, column=0, sticky='nsew', padx=75, pady=7)
    
    #api connections
    config = configparser.ConfigParser()
    config.read('config.ini')

    youtubeApiKey = config['API_KEYS']['youtubeApiKey']
    youtubeConnect = build('youtube', 'v3', developerKey=youtubeApiKey)
    # connects to youtube's public api

    spotifyApiKeyClientId = config['API_KEYS']['spotifyApiKeyClientId']
    spotifyApiKeyClientSecret = config['API_KEYS']['spotifyApiKeyClientSecret']
    spotifyRedirectUri = 'http://google.com/'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotifyApiKeyClientId, client_secret=spotifyApiKeyClientSecret, redirect_uri=spotifyRedirectUri))
    # connects to spotify's public api using spotipy library
else:
    frameForError.grid(row=0, column=0, sticky='nsew', padx=75, pady=7)

    iconLogo = tk.PhotoImage(file='icon logo.png')
    topLabel = tk.Label(frameForError, image=iconLogo, anchor='w', bg='#FFFFFF')
    topLabel.grid(row=0, column=0, pady=(30,10), sticky = "ew", )

    connectionErrorHeading = tk.Label(frameForError, text="connection error", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', fg='#B0B0B0')
    connectionErrorHeading.grid(row=1, column=0, pady=(260,0), sticky = "ew")

    connectionErrorText = tk.Label(frameForError, text="you are not connected to the internet, please do and restart the app", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', fg='#000000')
    connectionErrorText.grid(row=2, column=0, sticky = "ew")
# check bool value for internet connection and if it is disconnected, it will display a page with an error, or else, it will continue to set up the page






tableCreateQuery = '''
        CREATE TABLE IF NOT EXISTS releaseData (
            songTitle TEXT,
            releaseDate DATE,
            performedBy TEXT,
            writtenBy TEXT,
            prodBy TEXT,
            popTag TEXT,
            hiphopTag TEXT,
            indieTag TEXT,
            kpopTag TEXT,
            explicitTag TEXT,
            inhouseTag TEXT,
            lofiTag TEXT,
            artworkLocation TEXT,
            songFile TEXT,
            miscFiles TEXT,
            artworkImage BLOB,
            youtubeLink TEXT,
            spotifyLink TEXT
        )
        '''
# preset integer containing sql command for creation of database

isSongButtonClicked = False
isImageButtonClicked = False

def askForImage():
    global getImage
    while True:
        getImage = filedialog.askopenfilenames(title='select artwork', filetypes=(('png', "*.png"), ("jpg", "*.jpg")))
        if getImage:
            break
    global imageLocation
    imageLocation = str(getImage)[2:-3]

    if getImage:
        global photo
        photo = Image.open(getImage[0])

        resizedPhoto = photo.resize((140, 140))

        newPhoto = ImageTk.PhotoImage(resizedPhoto)

        importArtworkImage.image = newPhoto

        importArtworkImage.config(text='', image=newPhoto)
        global isImageButtonClicked
        isImageButtonClicked = True
# when called it shows the user a pop up window asking to select a png or jpg image file. upon gettingit, it will store its location and resize it to display inside the preview

def askForSong():
    global getSong
    while True:
        getSong = filedialog.askopenfilenames(title='select song', filetypes=(('mp3', "*.mp3"), ("wav", "*.wav")))
        if getSong:
            break  
    global songLocation
    maxLengthOfText = 45
    songLocation = str(getSong)[2:-3]
    global isSongButtonClicked
    isSongButtonClicked = True
    shortenedLocation = songLocation[:maxLengthOfText] + "..." if len(songLocation) > maxLengthOfText else songLocation
    importSong.config(text=shortenedLocation)
# when called it shows the user a pop up window asking to select a mp3 or wav song file. upon getting it, it will store the location of it and also shorten its location in order to preview it in its button

def convertImageIntoBinary(photo):
    with open(photo, 'rb') as file:
        PhotoImage = file.read() 
    return PhotoImage
# when called and inputted with an image, it will convert the image's file into a binary string

def showPage(frame):
    frame.tkraise()
# when called and inputted with the name of a frame, it will display that frame on the screen

def abbreviateNumber(value):
    value = int(value)
    if value >= 1000000000:
        return '{:.2f} B'.format(value/1000000000)
    elif value >= 1000000:
        return '{:.2f} M'.format(value/1000000)
    elif value >= 1000:
        return '{:.2f} K'.format(value/1000)
    else:
        return str(value)

showPage(frame)

def saveRelease(frame):
    songTitleValue = songTitle.get()
    releaseDateValue = releaseDate.get()
    performedByValue = performedBy.get()
    writtenByValue = writtenBy.get()
    prodByValue = prodBy.get()
    popVarValue = popVar.get()
    hiphopVarValue = hiphopVar.get()
    indieVarValue = indieVar.get()
    kpopVarValue = kpopVar.get()
    explicitVarValue = explicitVar.get()
    inhouseVarValue = inhouseVar.get()
    lofiVarValue = lofiVar.get()
    miscFilesText = addMiscFiles.get()
    # gets the value of the inputted values
    error = False

    if songTitleValue == "song title":
        error = True
    if releaseDate == "release date yyyy/mm/dd":
        error = True
    if performedByValue == 'performed by':
        error = True
    if writtenByValue == 'written by':
        error = True
    if prodByValue == 'produced by':
        error = True
    if miscFilesText == 'link to misc files':
        error = True
    # if their value is the same as their default value, error is raised

    if popVarValue == "NULL":
        popVarValue = None
    if hiphopVarValue == "NULL":
        hiphopVarValue = None
    if indieVarValue == "NULL":
        indieVarValue = None
    if kpopVarValue == "NULL":
        kpopVarValue = None
    if explicitVarValue == "NULL":
        explicitVarValue = None
    if inhouseVarValue == "NULL":
        inhouseVarValue = None
    if lofiVarValue == "NULL":
        lofiVarValue = None
    # if the value of tags is a NULL string, it will be changed to a python None
    

    global songLocation
    global getSong
    global isSongButtonClicked
    global isImageButtonClicked
    # sets them as global values

    if isImageButtonClicked == False:
        messagebox.showwarning('internal error', 'include artwork')
        # shows an error if the select image button was not interacted with
    else:
        if isSongButtonClicked == False:
            songLocation = None
            messagebox.showwarning('internal error', 'include song')
            # shows an error if the select song button was not interacted with
        else:
            isSongButtonClicked == True
            songLocation = str(getSong)[2:-3]
            if error == True:
                messagebox.showwarning('internal error', 'update default values for text')
                # shows an error if the default values for the input text was not changed
            else:
                if not miscFilesText.startswith('https://'):
                    messagebox.showwarning('internal error', 'misc files should be uploaded to a cloud drive and the web address should be stored')
                    # shows an error if the misc files input was not a website link
                else:
                    # if all the checks pass, it will continue to save the values to the database
                    conn = sqlite3.connect('data.db')
                    conn.execute(tableCreateQuery)
                    dataInsertQuery = '''
                        INSERT INTO releaseData(songTitle, releaseDate, performedBy, writtenBy, prodBy, popTag, hiphopTag, indieTag, kpopTag, explicitTag, inhouseTag, lofiTag, artworkLocation, songFile, miscFiles, artworkImage) 
                        VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', ?, ?, ?, ?)
                        '''.format(songTitleValue, releaseDateValue, performedByValue, writtenByValue, prodByValue, popVarValue, hiphopVarValue, indieVarValue, kpopVarValue, explicitVarValue, inhouseVarValue, lofiVarValue)
                    cursor = conn.cursor()
                    for image in getImage:
                        insertPhoto = convertImageIntoBinary(image)
                        cursor.execute(dataInsertQuery, (imageLocation, songLocation, miscFilesText, insertPhoto))
                    conn.commit()
                    conn.close()
                    # connects to database, saves values into their appropriate columns and closes the database
                    songFileName = songLocation.split("/")[-1]
                    shutil.copy(songLocation, 'databasefiles/')
                    # copies the song into a databasefiles folder

                    imageFileName = imageLocation.split("/")[-1]
                    print(imageFileName)
                    shutil.copy(imageLocation, 'databasefiles/')
                    # copies the image into a databasefiles folder

                    songTitle.delete(0, tk.END)
                    songTitle.insert(0, 'song title')
                    releaseDate.delete(0, tk.END)
                    releaseDate.insert(0, 'release date yyy/mm/dd')
                    performedBy.delete(0, tk.END)
                    performedBy.insert(0, 'performed by')
                    writtenBy.delete(0, tk.END)
                    writtenBy.insert(0, 'written by')
                    prodBy.delete(0, tk.END)
                    prodBy.insert(0, 'produced by')
                    addMiscFiles.delete(0, tk.END)
                    addMiscFiles.insert(0, 'link to misc files')
                    importArtworkImage.config(text='import artwork', image="", bg='#FFFFFF')
                    songLocation = None
                    isSongButtonClicked = False
                    isImageButtonClicked = False
                    popTag.deselect()
                    hiphopTag.deselect()
                    indieTag.deselect()
                    explicitTag.deselect()
                    kpopTag.deselect()
                    inhouseTag.deselect()
                    lofiTag.deselect()
                    addValuesToDB()
                    importSong.config(text='import song')
                    frame.tkraise()
                    # deletes all the added values from the input fields and replaces it back with the default text, preparing it for the next interaction
    
    


logo = tk.PhotoImage(file='mimic logo full.png')
topLabel = tk.Label(frame, image=logo, anchor='w', bg='#FFFFFF')
topLabel.grid(row=0, column=0, pady=(30,10), sticky = "ew", )
createRelease = tk.Button(frame, text="create release", font='"Space Grotesk" 13', width=78, anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, command=lambda: showPage(frame2), cursor='hand2')
createRelease.grid(row=1, column=0, pady=10, sticky = "ew")
previousReleases = tk.Frame(frame, bg='#FFFFFF',  borderwidth=1, relief='solid', width=78)
previousReleasesText = tk.Label(previousReleases, text='previous releases', font='"Space Grotesk" 13', anchor='w', padx=20, bg='#FFFFFF', foreground='#B0B0B0', pady=5)
previousReleasesText.grid(row=0,column=0, sticky = "ew")  
# lays out the elements for the main page

deleteImage = Image.open('delete button.png')
resizedDeleteImage = deleteImage.resize((17,17))
resizedDeleteImagePhotoImage = ImageTk.PhotoImage(resizedDeleteImage)
# creates an image element for the delete button to be used later on

def addValuesToDB():
    frame.tkraise()
    conn = sqlite3.connect('data.db')
    conn.execute(tableCreateQuery)
    cursor = conn.cursor()
    cursor.execute("SELECT songTitle from releaseData")
    fetchAllEntries = cursor.fetchall()
    conn.commit()
    global numberOfEntries
    numberOfEntries = len(fetchAllEntries)    
    conn.close()
    # connects to the database and finds the name of each song that has been inputted

    def createCommandForOpen(entry):
        return lambda: showEntryPage(entry)
    def createCommandForTracking(entry):
        return lambda: addTrackingForEntry(entry)
    def createCommandForYoutubeButton(entry):
        return lambda: youtubeButton(entry)
    def createCommandForSpotifyButton(entry):
        return lambda: spotifyButton(entry)
    # when called upon, they return their respective functions. they are used as passthrough because of a bug in tkinter which makes buttons not behalve properly when lambda functions are passed in directly to a button's command
    

    def youtubeButton(entry):
        webbrowser.open(entry)
    def spotifyButton(entry):
        webbrowser.open(entry)
    # when called upon and inputted with a link to a website, it opens the website in the default browser of the pc


    def addTrackingForEntry(recievedData):
        entry.destroy()
        deleteButton.destroy()
        addTrackingButton.destroy()
        backButtonTracking = tk.Button(frameForTracking, text="< back", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, command=lambda: [showPage(frame), addValuesToDB()], cursor='hand2', justify=tk.LEFT )
        backButtonTracking.grid(row=0, column=0, pady=30, sticky='w')

        songTitleTracking = tk.Label(frameForTracking, text=recievedData, relief='flat', font='"Space Grotesk" 13', width=39, fg='#000000', bg='#FFFFFF', justify=tk.LEFT, anchor='w')   
        songTitleTracking.grid(row=1,column=0, sticky = "nsew", padx=(0,50))

        trackingSection = tk.Label(frameForTracking, bg='#FFFFFF', activebackground='#FFFFFF')   

        trackYoutubeText = tk.Label(trackingSection, text='start tracking for Youtube', relief='flat', font='"Space Grotesk" 13', width=0, fg='#B0B0B0', bg='#FFFFFF', justify=tk.LEFT, anchor='w')   
        trackYoutubeText.grid(row=0,column=0, sticky = "nsew", padx=(0,7), pady=(10,0))

        trackYoutubeEntry = tk.Entry(trackingSection,relief='solid', font='"Space Grotesk" 13', width=54, fg='#000000', bg='#FFFFFF', justify=tk.LEFT, borderwidth=1)   
        trackYoutubeEntry.grid(row=0,column=1, sticky = "nsew", padx=(0,50), pady=(10,0))

        trackSpotifyText = tk.Label(trackingSection, text='                                      Spotify', relief='flat', font='"Space Grotesk" 13', width=0, fg='#B0B0B0', bg='#FFFFFF', justify=tk.LEFT, anchor='w')   
        trackSpotifyText.grid(row=1,column=0, sticky = "nsew", padx=(0,7), pady=(10,0))

        trackSpotifyEntry = tk.Entry(trackingSection,relief='solid', font='"Space Grotesk" 13', width=54, fg='#000000', bg='#FFFFFF', justify=tk.LEFT, borderwidth=1)   
        trackSpotifyEntry.grid(row=1,column=1, sticky = "nsew", padx=(0,50), pady=(10,0))

        saveTrackingButton = tk.Button(trackingSection, font='"Space Grotesk" 13', bg='#FFFFFF', text='start tracking', relief='flat', activebackground='#FFFFFF', borderwidth=0, cursor='hand2', command=lambda: saveTracking(recievedData, trackYoutubeEntry, trackSpotifyEntry))
        saveTrackingButton.grid(row= 2, column=1, pady=(155,0), padx=(0,44), sticky='e')

        trackingSection.grid(row=2, column=0)
        frameForTracking.tkraise()
        # when the add tracking button is clicked for an entry, a new page is created to recieve the youtube and spotify links of that song


    global totalYoutubeCount
    global totalSpotifyCount
    global numberOfEntriesWithAnalytics
    numberOfEntriesWithAnalytics = 0
    totalYoutubeCount = 0
    totalSpotifyCount = 0
    # initializes global values and sets them to 0 to be used later


    if numberOfEntries == 0:
            noReleasesText = tk.Label(previousReleases, text='there are no releases at the moment', font='"Space Grotesk" 13', anchor='w', padx=20, bg='#FFFFFF', foreground='#000000', pady=5)
            noReleasesText.grid(row=1,column=0, sticky = "ew")  
            # if there are no entries to the database yet, it will tell the user that there are no releases at the moment
    else:
        # if there are entries in the database, it will go through each entry and create its respective ui element in the previous releases section of the main page
        for i in range(numberOfEntries):

            def createCommandForDeleteWithAnalytics(entry):
                return lambda: deleteEntryWithAnalytics(entry)

            def deleteEntryWithAnalytics(recievedData):
                deleteReleaseQuestion = tk.messagebox.askquestion('delete release', 'you sure you want to delete this release?', icon='warning')
                if deleteReleaseQuestion == 'yes':
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()
                    deleteValuesFromTable = '''DELETE FROM releaseData WHERE songTitle = ?'''
                    cursor.execute(deleteValuesFromTable, (str(recievedData),))
                    conn.commit()
                    conn.close()
                    addValuesToDB()
                    restart()
                    # entry.destroy()
                    # deleteButton.destroy()
                    # addTrackingButton.destroy()
                    # youtubeAnalytics.destroy()
                    # spotifyAnalytics.destroy()

            def createCommandForDeleteWithoutAnalytics(entry):
                return lambda: deleteEntryWithoutAnalytics(entry)

            def deleteEntryWithoutAnalytics(recievedData):
                deleteReleaseQuestion = tk.messagebox.askquestion('delete release', 'you sure you want to delete this release?', icon='warning')
                if deleteReleaseQuestion == 'yes':
                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()
                    deleteValuesFromTable = '''DELETE FROM releaseData WHERE songTitle = ?'''
                    cursor.execute(deleteValuesFromTable, (str(recievedData),))
                    conn.commit()
                    conn.close()
                    addValuesToDB()
                    restart()
                    # entry.destroy()
                    # deleteButton.destroy()
                    # addTrackingButton.destroy()
            
            # previous functions when run will delete the values from the database and run the restart function in order to restart the app with fresh values
            # we are having to restart the app due to a bug in tkinter which does not allow the ui to fully refresh itself whenever the addValuesToDB() function is
            # called upon when deleted.


            fetchEntry = fetchAllEntries[i]
            # for each interation of the loop fetchEntry with have the name of that song
            fetchEntry = str(fetchEntry)[2:-3]

            
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT youtubeLink,spotifyLink from releaseData")
            fetchTrackingLinks = cursor.fetchall()
            conn.commit()
            conn.close()
            youtubeLinkFetch = fetchTrackingLinks[i][0]
            spotifyLinkFetch = fetchTrackingLinks[i][1]
            # will fetch the values of youtube and spotify links in their database
            
            if youtubeLinkFetch != None:
                # if a link is found it will do the following
                entry = tk.Button(previousReleases, text=fetchEntry, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5, borderwidth=0, width=62, cursor='hand2', command=createCommandForOpen(fetchEntry))
                entry.grid(row=i+1, column=0, sticky="w", pady=(0,3))

                youtubeVideoId = youtubeLinkFetch.find("?v=") + len("?v=")
                youtubeVideoId = youtubeLinkFetch[youtubeVideoId:youtubeVideoId+11]
                youtubeRequest = youtubeConnect.videos().list(
                    part='statistics',
                    id=youtubeVideoId
                )
                youtubeResponse = youtubeRequest.execute()
                youtubeViewCount = youtubeResponse['items'][0]['statistics']['viewCount']
                # it will request the number of views of that video from youtube's api


                youtubeViewCount = int(youtubeViewCount)
                totalYoutubeCount = totalYoutubeCount + youtubeViewCount
                youtubeViewCount = abbreviateNumber(youtubeViewCount)

                spotifyTrackId = spotifyLinkFetch.find("/track/") + len("/track/")
                spotifyTrackId = spotifyLinkFetch[spotifyTrackId:spotifyTrackId+22]
                spotifyTrackInfo = sp.track(spotifyTrackId)
                spotifySongPopularity = spotifyTrackInfo['popularity']
                spotifySongPopularity = int(spotifySongPopularity)
                totalSpotifyCount = totalSpotifyCount + spotifySongPopularity
                # it will request the popularity of that song from spotify's api
                # we are not able to get the number of plays of that spotify track since spotify's public api does not offer the functionality


                addTrackingButton = tk.Label(previousReleases, font='"Space Grotesk" 11', bg='#FFFFFF', padx=14, pady=0, borderwidth=0, relief='flat', width=12, height=3, text='')
                youtubeAnalytics = tk.Button(addTrackingButton, font='"Space Grotesk" 11', anchor='e', bg='#FFFFFF', padx=15, pady=5, borderwidth=0, relief='flat', foreground='#FE0404', text=youtubeViewCount, command=createCommandForYoutubeButton(youtubeLinkFetch), cursor='hand2', width=5)
                youtubeAnalytics.grid(row=0, column=0, pady=(0,3))
                spotifyAnalytics = tk.Button(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=10, pady=5, borderwidth=0, relief='flat', foreground='#1DD05D', text=spotifySongPopularity, command=createCommandForSpotifyButton(spotifyLinkFetch), cursor='hand2', width=3)
                spotifyAnalytics.grid(row=0, column=1, pady=(0,3), padx=(3,0))
                addTrackingButton.grid(row=i+1, column=1, sticky='w', columnspan=2, padx=(20,0), pady=(0,3))
                deleteButton = tk.Button(previousReleases, image=resizedDeleteImagePhotoImage, cursor='hand2', relief='solid', borderwidth=1, background='#FFFFFF', activebackground='#FFFFFF', command=createCommandForDeleteWithAnalytics(fetchEntry), width=29, height=29)
                deleteButton.image = resizedDeleteImagePhotoImage
                deleteButton.grid(row=i+1, column=3, sticky='w', padx=(20,15), pady=(0,3))
                numberOfEntriesWithAnalytics = numberOfEntriesWithAnalytics + 1
                # it will add add the value of the youtube views and spotify popularity in place of the add analytics button, it will also be clickable which will open that website


            else:
                # if no tracking is found it will create an add analytics button and do the following

                def createCommandForSavingTracking(recievedData, trackYoutubeEntry, trackSpotifyEntry):
                    return lambda: saveTracking(recievedData, trackYoutubeEntry, trackSpotifyEntry)

                def saveTracking(recievedData, trackYoutubeEntry, trackSpotifyEntry):
                    # when this is called and supplied with the tracking data that the user enters, it will do the following
                    entry.destroy()
                    deleteButton.destroy()
                    addTrackingButton.destroy()
                    youtubeLinkValue = trackYoutubeEntry.get()
                    spotifyLinkValue = trackSpotifyEntry.get()  
                    errorTracking = False
                    if youtubeLinkValue == '':
                        errorTracking = True
                    if spotifyLinkValue == '':
                        errorTracking = True
                    if not youtubeLinkValue.startswith('https://www.youtube.com/watch?v'):
                        errorTracking = True
                    if not spotifyLinkValue.startswith('https://open.spotify.com/track'):
                        errorTracking = True
                    
                    # it will check if the link is an actual youtube / spotify link
                    if errorTracking == True:
                        messagebox.showwarning('internal error', 'links should be in proper format, for ex \n\nyoutube\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ\n\nspotify\nhttps://open.spotify.com/track/4PTG3Z6ehGkBFwjyb...')
                    else:
                        conn = sqlite3.connect('data.db')
                        # it will add that youtube and spotify link to its respective place
                        addTrackingToTable = '''UPDATE releaseData SET youtubeLink = ?, spotifyLink = ? WHERE songTitle = ?'''
                        cursor = conn.cursor()
                        cursor.execute(addTrackingToTable, (youtubeLinkValue, spotifyLinkValue, recievedData))
                        conn.commit()
                        cursor.execute("SELECT youtubeLink,spotifyLink from releaseData")
                        fetchTrackingLinks = cursor.fetchall()
                        conn.commit()
                        conn.close()
                        frame.tkraise()
                        addValuesToDB()

                entry = tk.Button(previousReleases, text=fetchEntry, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5, borderwidth=0, width=62, cursor='hand2', command=createCommandForOpen(fetchEntry))
                entry.grid(row=i+1, column=0, sticky="w", pady=(0,3))

                addTrackingButton = tk.Button(previousReleases, text='add tracking', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=14, pady=0, borderwidth=1, cursor='hand2', relief='solid', command=createCommandForTracking(fetchEntry), activebackground='#FFFFFF')
                addTrackingButton.grid(row=i+1, column=1, sticky='w', columnspan=2, padx=(20,0), pady=(0,3))
                deleteButton = tk.Button(previousReleases, image=resizedDeleteImagePhotoImage, cursor='hand2', relief='solid', borderwidth=1, background='#FFFFFF', activebackground='#FFFFFF', command=createCommandForDeleteWithoutAnalytics(fetchEntry), width=29, height=29)
                deleteButton.image = resizedDeleteImagePhotoImage
                deleteButton.grid(row=i+1, column=3, sticky='w', padx=(20,10), pady=(0,3))
                # creates the entry value, add tracking and delete button bounded to their specific functions


    previousReleases.grid(row=2,column=0, sticky = "ew", pady=10)
    # it closes the previous releases section over here

    viewAnalytics = tk.Button(frame, text="view analytics", font='"Space Grotesk" 13', anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, cursor='hand2', command=lambda: showPage(frameForAnalytics))
    viewAnalytics.grid(row=3, column=0, pady=10, sticky = "swe")
    # the view analytics button is created


    ### THE VIEW ANALYTICS PAGE

    if numberOfEntriesWithAnalytics == 0:
        # if the page is opened and there is no tracking data added yet, it will create a page showing an error
        backButton = tk.Button(frameForErrorNoAnalytics, text="< back", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, command=lambda: showPage(frame), cursor='hand2', justify=tk.LEFT )
        backButton.grid(row=0, column=0, pady=(30,10), sticky='w')

        noAnalyticsErrorHeading = tk.Label(frameForErrorNoAnalytics, text="analytics error", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', fg='#B0B0B0')
        noAnalyticsErrorHeading.grid(row=1, column=0, pady=(260,0), sticky = "ew")

        noAnalyticsErrorText = tk.Label(frameForErrorNoAnalytics, text="tracking hasn't been added to any entries, please do and check back later", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', fg='#000000')
        noAnalyticsErrorText.grid(row=2, column=0, sticky = "ew")
        viewAnalytics.config(command=lambda: showPage(frameForErrorNoAnalytics))
    else:
        # if there are values in the database with tracking added to them, it will do the following
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        selectValuesFromTableForAnalysis = '''SELECT songTitle,youtubeLink,spotifyLink,popTag,hiphopTag,indieTag,kpopTag,explicitTag,inhouseTag,lofiTag FROM releaseData WHERE youtubeLink IS NOT NULL'''
        cursor.execute(selectValuesFromTableForAnalysis)
        fetchDataForAnalysis = cursor.fetchall()
        conn.commit()
        conn.close()
        # it will connect to the database and fetch the required values that we will use to analyze the data
        analyticsDataForGraphs = []
        # creating an empty list to which values will be added later and which we will later convert into a pandas dataframe

        for j in range(len(fetchDataForAnalysis)):
            # for each entry it will fetch the required values
            songTitleForAnalysis = fetchDataForAnalysis[j][0]
            youtubeLinkForAnalysis = fetchDataForAnalysis[j][1]
            spotifyLinkForAnalysis = fetchDataForAnalysis[j][2]

            popTagForAnalysis = fetchDataForAnalysis[j][3]
            hiphopTagForAnalysis = fetchDataForAnalysis[j][4]
            indieTagForAnalysis = fetchDataForAnalysis[j][5]
            kpopTagForAnalysis = fetchDataForAnalysis[j][6]
            explicitTagForAnalysis = fetchDataForAnalysis[j][7]
            inhouseTagForAnalysis = fetchDataForAnalysis[j][8]
            lofiTagForAnalysis = fetchDataForAnalysis[j][9]

            youtubeVideoId = youtubeLinkForAnalysis.find("?v=") + len("?v=")
            youtubeVideoId = youtubeLinkForAnalysis[youtubeVideoId:youtubeVideoId+11]
            youtubeRequest = youtubeConnect.videos().list(
                part='statistics',
                id=youtubeVideoId
            )
            youtubeResponse = youtubeRequest.execute()
            youtubeViewCount = youtubeResponse['items'][0]['statistics']['viewCount']
            youtubeViewCount = int(youtubeViewCount)
            youtubeViewCount = "{:,}".format(youtubeViewCount)

            spotifyTrackId = spotifyLinkForAnalysis.find("/track/") + len("/track/")
            spotifyTrackId = spotifyLinkForAnalysis[spotifyTrackId:spotifyTrackId+22]
            spotifyTrackInfo = sp.track(spotifyTrackId)
            spotifySongPopularity = spotifyTrackInfo['popularity']
            spotifySongPopularity = int(spotifySongPopularity)

            # it calls the youtube and spotify api again to get their values then store them into variables

            analyticsDataForGraphs.append([songTitleForAnalysis, youtubeViewCount, spotifySongPopularity, popTagForAnalysis, hiphopTagForAnalysis, indieTagForAnalysis, kpopTagForAnalysis, explicitTagForAnalysis, inhouseTagForAnalysis, lofiTagForAnalysis])
            # all the required values are added to the list

        avgYoutubeViewsNumberWithCommas = 0
        avgSpotifyPopularityNumber = 0

        backButton = tk.Button(frameForAnalytics, text="< back", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, command=lambda: showPage(frame), cursor='hand2', justify=tk.LEFT )
        backButton.grid(row=0, column=0, pady=(30,0), sticky='w')

        avgYoutubeViewsText = tk.Label(frameForAnalytics, font='"Space Grotesk" 13', fg='#B0B0B0', bg='#FFFFFF', text='avg youtube views', anchor='sw', padx=5, pady=5, width=18)
        avgYoutubeViewsText.grid(row=1,column=0, sticky = "nsew", padx=(0,50))  

        avgYoutubeViewsNumber = int(totalYoutubeCount/numberOfEntriesWithAnalytics)
        avgYoutubeViewsNumberWithCommas = "{:,}".format(avgYoutubeViewsNumber)
        avgSpotifyPopularityNumber = int(totalSpotifyCount/numberOfEntriesWithAnalytics)

        avgYoutubeViews = tk.Label(frameForAnalytics, font='"Space Grotesk" 21', width=8, fg='#000000', bg='#FFFFFF', text=avgYoutubeViewsNumberWithCommas, anchor='e', padx=5, pady=5)
        avgYoutubeViews.grid(row=1,column=1, sticky = "nsew", padx=(0,50))  

        avgSpotifyPopularityText = tk.Label(frameForAnalytics, font='"Space Grotesk" 13',fg='#B0B0B0', bg='#FFFFFF', text='avg spotify popularity', anchor='sw', padx=5, pady=5, width=18)
        avgSpotifyPopularityText.grid(row=1,column=2, sticky = "nsew", padx=(0,40))  

        avgSpotifyPopularity = tk.Label(frameForAnalytics, font='"Space Grotesk" 21', width=8, fg='#000000', bg='#FFFFFF', text=avgSpotifyPopularityNumber, anchor='e', padx=5, pady=5)
        avgSpotifyPopularity.grid(row=1,column=3, sticky = "nsew", padx=(0,40))  
        # the base ui for the analytics page is created


        analyticsDataForGraphs = pd.DataFrame(analyticsDataForGraphs, columns=['song title', 'youtube views', 'spotify popularity', 'pop', 'hiphop', 'indie', 'kpop', 'explicit', 'inhouse', 'lofi'])
        analyticsDataForGraphs.to_csv('analyticsData.csv')
        # the list that we created earlier is now converted into a pandas database with its custom column names and is also saved as a csv which can be used
        # for external uses

        analyticsDataForScatterPlot = analyticsDataForGraphs.drop(['pop', 'hiphop', 'indie', 'kpop', 'explicit', 'inhouse', 'lofi'], axis=1)
        dataFrameScatterPlot = pd.DataFrame(analyticsDataForScatterPlot)
        # we are setting up the values for creating a scatter plot which shows the number of youtube views and spotify popularity number on a graph with 
        # each point representing each song, for this we do not require the tag values


        def onCanvasClick(event):
            # this is a function that when interacted will open the generated matplotlib graph in full screen
            fullScreenScatter = Toplevel()
            fullScreenScatter.title('full screen plot')
            scatterFig = Figure(figsize=(12, 8), dpi=100)
            ax = scatterFig.add_subplot(111)   

            factorizeColor, labels = pd.factorize(dataFrameScatterPlot['song title'])
            scatter = ax.scatter(dataFrameScatterPlot['youtube views'], dataFrameScatterPlot['spotify popularity'], c=factorizeColor, cmap=cm.viridis, label=dataFrameScatterPlot['song title'])
            ax.legend(scatter.legend_elements()[0], labels)
            ax.set_xlabel('youtube views')
            ax.set_ylabel('spotify popularity')

            canvas = FigureCanvasTkAgg(scatterFig, master=fullScreenScatter)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            toolbar = NavigationToolbar2Tk(canvas, fullScreenScatter)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            fullScreenScatter.attributes('-fullscreen', True)
            fullScreenScatter.bind('<Escape>', lambda event: fullScreenScatter.destroy())


        scatterFig = Figure(figsize=(6,4), dpi=70)
        ax = scatterFig.add_subplot(111)

        factorizeColor, labels = pd.factorize(dataFrameScatterPlot['song title'])
        scatter = ax.scatter(dataFrameScatterPlot['youtube views'], dataFrameScatterPlot['spotify popularity'], c=factorizeColor, cmap=cm.viridis, label=dataFrameScatterPlot['song title'])
        # if numberOfEntriesWithAnalytics != 0:
        ax.legend(scatter.legend_elements()[0], labels, loc='lower right')
        ax.set_xlabel('youtube views')
        ax.set_ylabel('spotify popularity')

        canvas = FigureCanvasTkAgg(scatterFig, master=frameForAnalytics)
        canvas.get_tk_widget().grid(row=2, column=0, sticky='nw', columnspan=2)
        canvas.mpl_connect('button_press_event', onCanvasClick)
        # this will create a matplotlib scatter point graph with the data that we have given it. upon clicking on the graph, it will open the same graph in fullscreen
        # along with showing the default matplotlib controls



        popValueForAnalyticsTotalYoutube = 0
        hiphopValueForAnalyticsTotalYoutube = 0
        indieValueForAnalyticsTotalYoutube = 0
        kpopValueForAnalyticsTotalYoutube = 0
        explicitValueForAnalyticsTotalYoutube = 0
        inhouseValueForAnalyticsTotalYoutube = 0
        lofiValueForAnalyticsTotalYoutube = 0

        popValueForAnalyticsTotalSpotify = 0
        hiphopValueForAnalyticsTotalSpotify = 0
        indieValueForAnalyticsTotalSpotify = 0
        kpopValueForAnalyticsTotalSpotify = 0
        explicitValueForAnalyticsTotalSpotify = 0
        inhouseValueForAnalyticsTotalSpotify = 0
        lofiValueForAnalyticsTotalSpotify = 0

        # this initializes the values for the tags as zero in order for the next graph to work

        errorStacked = True
        stackedPlotData = []
        # this creates a new empty list which will then have values added to it which will then be converted to a pandas dataframe

        for m in range(len(analyticsDataForGraphs)):
            # it will go through this command for the number of entries that are in it

            popValueForAnalytics = analyticsDataForGraphs.loc[m, 'pop']
            hiphopValueForAnalytics = analyticsDataForGraphs.loc[m, 'hiphop']
            indieValueForAnalytics = analyticsDataForGraphs.loc[m, 'indie']
            kpopValueForAnalytics = analyticsDataForGraphs.loc[m, 'kpop']
            explicitValueForAnalytics = analyticsDataForGraphs.loc[m, 'explicit']
            inhouseValueForAnalytics = analyticsDataForGraphs.loc[m, 'inhouse']
            lofiValueForAnalytics = analyticsDataForGraphs.loc[m, 'lofi']
            # it will locate the values of the tags for each entry in the analyticsDataForGraphs pandas dataframe that we created earlier
            # and bind it to a variable

            if popValueForAnalytics != 'None':
                popValueForAnalyticsTotalYoutube = int(analyticsDataForGraphs.loc[m, 'youtube views'].replace(",", "")) + int(popValueForAnalyticsTotalYoutube)
                popValueForAnalyticsTotalSpotify = int(analyticsDataForGraphs.loc[m, 'spotify popularity']) + int(popValueForAnalyticsTotalSpotify)
                errorStacked = False

            if hiphopValueForAnalytics != 'None':
                hiphopValueForAnalyticsTotalYoutube = int(analyticsDataForGraphs.loc[m, 'youtube views'].replace(",", "")) + int(hiphopValueForAnalyticsTotalYoutube)
                hiphopValueForAnalyticsTotalSpotify = int(analyticsDataForGraphs.loc[m, 'spotify popularity']) + int(hiphopValueForAnalyticsTotalSpotify)
                errorStacked = False

            if indieValueForAnalytics != 'None':
                indieValueForAnalyticsTotalYoutube = int(analyticsDataForGraphs.loc[m, 'youtube views'].replace(",", "")) + int(indieValueForAnalyticsTotalYoutube)
                indieValueForAnalyticsTotalSpotify = int(analyticsDataForGraphs.loc[m, 'spotify popularity']) + int(indieValueForAnalyticsTotalSpotify)
                errorStacked = False

            if kpopValueForAnalytics != 'None':
                kpopValueForAnalyticsTotalYoutube = int(analyticsDataForGraphs.loc[m, 'youtube views'].replace(",", "")) + int(kpopValueForAnalyticsTotalYoutube)
                kpopValueForAnalyticsTotalSpotify = int(analyticsDataForGraphs.loc[m, 'spotify popularity']) + int(kpopValueForAnalyticsTotalSpotify)
                errorStacked = False

            if explicitValueForAnalytics != 'None':
                explicitValueForAnalyticsTotalYoutube = int(analyticsDataForGraphs.loc[m, 'youtube views'].replace(",", "")) + int(explicitValueForAnalyticsTotalYoutube)
                explicitValueForAnalyticsTotalSpotify = int(analyticsDataForGraphs.loc[m, 'spotify popularity']) + int(explicitValueForAnalyticsTotalSpotify)
                errorStacked = False

            if inhouseValueForAnalytics != 'None':
                inhouseValueForAnalyticsTotalYoutube = int(analyticsDataForGraphs.loc[m, 'youtube views'].replace(",", "")) + int(inhouseValueForAnalyticsTotalYoutube)
                inhouseValueForAnalyticsTotalSpotify = int(analyticsDataForGraphs.loc[m, 'spotify popularity']) + int(inhouseValueForAnalyticsTotalSpotify)
                errorStacked = False

            if lofiValueForAnalytics != 'None':
                lofiValueForAnalyticsTotalYoutube = int(analyticsDataForGraphs.loc[m, 'youtube views'].replace(",", "")) + int(lofiValueForAnalyticsTotalYoutube)
                lofiValueForAnalyticsTotalSpotify = int(analyticsDataForGraphs.loc[m, 'spotify popularity']) + int(lofiValueForAnalyticsTotalSpotify)
                errorStacked = False

            # each tag's value will be checked to see if it is empty or not. if it is not, its value will be added to the total at each iteration of the loop
            
        if errorStacked == False:
            stackedPlotData.append([popValueForAnalyticsTotalYoutube, hiphopValueForAnalyticsTotalYoutube, indieValueForAnalyticsTotalYoutube, kpopValueForAnalyticsTotalYoutube, explicitValueForAnalyticsTotalYoutube, inhouseValueForAnalyticsTotalYoutube, lofiValueForAnalyticsTotalYoutube])
            stackedPlotData.append([popValueForAnalyticsTotalSpotify, hiphopValueForAnalyticsTotalSpotify, indieValueForAnalyticsTotalSpotify, kpopValueForAnalyticsTotalSpotify, explicitValueForAnalyticsTotalSpotify, inhouseValueForAnalyticsTotalSpotify, lofiValueForAnalyticsTotalSpotify])          
            dataFrameStackedPlot = pd.DataFrame({'tags': ['pop', 'hiphop', 'indie', 'kpop', 'explicit', 'inhouse', 'lofi'], 'youtube views': stackedPlotData[0], 'spotify popularity': stackedPlotData[1]})              
            # if there ar eno errors, it will create the final dataframe which we can use in matplotlib and add values to it


        def onCanvasClick2(event):
            # this is another full screen function which will open the created graph in fullscreen when clicked
            fullScreenStacked = Toplevel()
            fullScreenStacked.title('full screen plot')

            cmap = plt.cm.get_cmap('YlGn')
            stackedFig = Figure(figsize=(6.3,4), dpi=70)
            ax = stackedFig.add_subplot(111)
            ax.bar(dataFrameStackedPlot['tags'], dataFrameStackedPlot['youtube views'], color=cmap(dataFrameStackedPlot['spotify popularity']))
            ax.set_xlabel('tags')
            ax.set_ylabel('youtube views')
            sm = plt.cm.ScalarMappable(cmap=cmap)
            sm.set_array(dataFrameStackedPlot['youtube views'])
            plt.colorbar(sm)

            canvas = FigureCanvasTkAgg(stackedFig, master=fullScreenStacked)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            toolbar = NavigationToolbar2Tk(canvas, fullScreenStacked)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            fullScreenStacked.attributes('-fullscreen', True)
            fullScreenStacked.bind('<Escape>', lambda event: fullScreenStacked.destroy())


        # this is the code for a stacked bar graph which will make 7 bars, each for each tag, it will determine the height of each bar
        # based on the total number of youtube views that it has accumulated
        # the color of each bar is based on the spotify popularity of the song. the darker it is, the more popular it is on spotify
        cmap = plt.cm.get_cmap('YlGn')
        stackedFig = Figure(figsize=(6.3,4), dpi=70)
        ax = stackedFig.add_subplot(111)
        ax.bar(dataFrameStackedPlot['tags'], dataFrameStackedPlot['youtube views'], color=cmap(dataFrameStackedPlot['spotify popularity']))
        ax.set_xlabel('tags')
        ax.set_ylabel('youtube views')
        sm = plt.cm.ScalarMappable(cmap=cmap)
        sm.set_array(dataFrameStackedPlot['youtube views'])
        plt.colorbar(sm)

        canvas = FigureCanvasTkAgg(stackedFig, master=frameForAnalytics)
        canvas.get_tk_widget().grid(row=2, column=2, columnspan=2)
        canvas.mpl_connect('button_press_event', onCanvasClick2)

addValuesToDB()



### ADD RELEASES PAGE

# this is the ui for the add releases page, when a user clicks on the page to add a release, this ui will be generated
# it is based on a grid system with seperate rows and colums for each element

backButton = tk.Button(frame2, text="< back", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, command=lambda: showPage(frame), cursor='hand2', justify=tk.LEFT )
backButton.grid(row=0, column=0, pady=30, sticky='w')
splitGrid = tk.Label(frame2, bg='#FFFFFF',  borderwidth=0, relief='flat')
#col1
songTitle = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
songTitle.grid(row=1,column=0, sticky = "nsew", padx=(0,50))  
songTitle.insert(0, "song title")
tags = tk.Label(splitGrid, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='left')
#first row
popVar = tk.StringVar()
popTag = CTkCheckBox(tags, text="pop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=popVar, onvalue='pop', offvalue='NULL', hover=False, fg_color='#000000')
popTag.deselect()
popTag.grid(row=0, column=0, sticky='w')
hiphopVar = tk.StringVar()
hiphopTag = CTkCheckBox(tags, text="hip hop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=hiphopVar, onvalue='hiphop', offvalue='NULL', hover=False, fg_color='#000000')
hiphopTag.deselect()
hiphopTag.grid(row=0, column=1 , sticky='w')
indieVar = tk.StringVar()
indieTag = CTkCheckBox(tags, text="indie", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=indieVar, onvalue='indie', offvalue='NULL', hover=False, fg_color='#000000')
indieTag.deselect()
indieTag.grid(row=0, column=2 , sticky='w')
kpopVar = tk.StringVar()
kpopTag = CTkCheckBox(tags, text="kpop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=kpopVar, onvalue='kpop', offvalue='NULL', hover=False, fg_color='#000000')
kpopTag.deselect()
kpopTag.grid(row=0, column=3 , sticky='w')
#second row
explicitVar = tk.StringVar()
explicitTag = CTkCheckBox(tags, text="explicit", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=explicitVar, onvalue='explicit', offvalue='NULL', hover=False, fg_color='#000000')
explicitTag.deselect()
explicitTag.grid(row=1, column=0, sticky='w')
inhouseVar = tk.StringVar()
inhouseTag = CTkCheckBox(tags, text="inhouse", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=inhouseVar, onvalue='inhouse', offvalue='NULL', hover=False, fg_color='#000000')
inhouseTag.deselect()
inhouseTag.grid(row=1, column=1, sticky='w')
lofiVar = tk.StringVar()
lofiTag = CTkCheckBox(tags, text="lofi", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=lofiVar, onvalue='lofi', offvalue='NULL', hover=False, fg_color='#000000')
lofiTag.deselect()
lofiTag.grid(row=1, column=2, sticky='w')
tags.grid(row=2, column=0, sticky='w', pady=(15,0))
importsGrid = tk.Label(splitGrid, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='left')
##
importArtworkImage = tk.Button(importsGrid, text="import artwork", font='"Space Grotesk" 13', anchor='sw', bg='#FFFFFF',fg='#B0B0B0', relief='solid', borderwidth=1, activebackground='#FFFFFF',activeforeground='#B0B0B0', cursor='hand2', justify=tk.LEFT, command=askForImage)
importArtworkImage.grid(row=0, column=0, sticky='news', padx=(0,20))
importsGridInside = tk.Label(importsGrid, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='right')
##
importSong = tk.Button(importsGridInside, text="import song", font='"Space Grotesk" 13', anchor='sw', bg='#FFFFFF',fg='#B0B0B0', relief='solid', borderwidth=1, activebackground='#FFFFFF',activeforeground='#B0B0B0',  cursor='hand2', justify=tk.LEFT, height=3, command=askForSong, wraplength=210)
importSong.grid(row=0,column=0, sticky='news', pady=(0,19))
##
addMiscFiles = tk.Entry(importsGridInside, borderwidth=1, relief='solid', font='"Space Grotesk" 13', fg='#B0B0B0')
addMiscFiles.grid(row=1,column=0, sticky = "nsew")  
addMiscFiles.insert(0, "link to misc files")
importsGridInside.grid(row=0, column=1, padx=(10,0), sticky='e')
importsGrid.grid(row=3, column=0, sticky='w', pady=(20,0), rowspan=3)

#col2
releaseDate = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
releaseDate.grid(row=1,column=1, sticky = "nsew")
releaseDate.insert(0, "release date yyyy/mm/dd")
performedBy = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
performedBy.grid(row=3,column=1, sticky = "nsew", pady=(20,0))
performedBy.insert(0, "performed by")
writtenBy = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
writtenBy.grid(row=4,column=1, sticky = "nsew", pady=(15,0))
writtenBy.insert(0, "written by")
prodBy = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
prodBy.grid(row=5,column=1, sticky = "nsew", pady=(15,0))
prodBy.insert(0, "produced by")

saveReleaseButton = tk.Button(splitGrid, font='"Space Grotesk" 13', bg='#FFFFFF', text='save release', relief='flat', activebackground='#FFFFFF', command=lambda: [saveRelease(frame), convertImageIntoBinary(photo)], borderwidth=0, cursor='hand2')
saveReleaseButton.grid(row= 6, column=1, pady=(20,0), sticky='e')
splitGrid.grid(row=1, column=0, sticky='ew')
# when the save release button is clicked, the saveRelease function is called and that is when the rest of the previously created commands run


### VIEW RELEASES PAGE

# after a release is created an it is viewable in the previous releases section, the user is able to click on the name of the song to view everything that 
# they had previously entered. all the values are greyed out and thus they are not able to edit anything
def showEntryPage(recievedData):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    selectValuesFromTable = '''SELECT * FROM releaseData WHERE songTitle = ?'''
    cursor.execute(selectValuesFromTable, (str(recievedData),))
    fetchAllEntries = cursor.fetchall()
    conn.commit()
    conn.close()
    # it will connect to the database again and get all the values in the database related to the name of the song clicked

    songTitleTempValue, releaseDateTempValue, performedByTempValue, writtenByTempValue, prodByTempValue, popVarTempValue, hiphopVarTempValue, indieVarTempValue, kpopVarTempValue, explicitVarTempValue, inhouseVarTempValue, lofiVarTempValue, ArtworkImageLocationTempValue, importSongTempValue, addMiscFilesTempValue, importArtworkImageTempValue, youtubeLinkTemp, spotifyLinkTemp = fetchAllEntries[0]
    maxLengthOfTextTemp = 45
    songShortenedLocationTemp = importSongTempValue[:maxLengthOfTextTemp] + "..." if len(importSongTempValue) > maxLengthOfTextTemp else importSongTempValue
    maxLengthOfMiscTextTemp = 20
    addMiscFilesTempValueShortened = addMiscFilesTempValue[:maxLengthOfMiscTextTemp] + "..." if len(addMiscFilesTempValue) > maxLengthOfMiscTextTemp else addMiscFilesTempValue
    stream = io.BytesIO(importArtworkImageTempValue)
    image = Image.open(stream)
    resizedPhoto = image.resize((140, 140))
    global newPhotoTemp
    newPhotoTemp = ImageTk.PhotoImage(resizedPhoto)
    tempFrameForEntry.tkraise()
    backButtonTemp = tk.Button(tempFrameForEntry, text="< back", font='"Space Grotesk" 13', anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, cursor='hand2', command=lambda: showPage(frame))
    backButtonTemp.grid(row=0, column=0, pady=30, sticky='w')
    splitGridTemp = tk.Label(tempFrameForEntry, bg='#FFFFFF',  borderwidth=0, relief='flat')
    #col1
    songTitleTemp = tk.Label(splitGridTemp, text=songTitleTempValue, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=39, fg='#B0B0B0', bg='#FFFFFF', justify=tk.LEFT, anchor='w')
    songTitleTemp.grid(row=0,column=0, sticky = "nsew", padx=(0,50))  
    tagsTemp = tk.Label(splitGridTemp, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='left')
    #first row
    popVarTemp = tk.StringVar()
    popTagTemp = CTkCheckBox(tagsTemp, text="pop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=popVarTemp, onvalue='pop', offvalue='NULL', hover=False, fg_color='#000000')
    popTagTemp.deselect()
    popTagTemp.grid(row=0, column=0, sticky='w')
    hiphopVarTemp = tk.StringVar()
    hiphopTagTemp = CTkCheckBox(tagsTemp, text="hip hop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=hiphopVarTemp, onvalue='hiphop', offvalue='NULL', hover=False, fg_color='#000000')
    hiphopTagTemp.deselect()
    hiphopTagTemp.grid(row=0, column=1 , sticky='w')
    indieVarTemp = tk.StringVar()
    indieTagTemp = CTkCheckBox(tagsTemp, text="indie", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=indieVarTemp, onvalue='indie', offvalue='NULL', hover=False, fg_color='#000000')
    indieTagTemp.deselect()
    indieTagTemp.grid(row=0, column=2 , sticky='w')
    kpopVarTemp = tk.StringVar()
    kpopTagTemp = CTkCheckBox(tagsTemp, text="kpop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=kpopVarTemp, onvalue='kpop', offvalue='NULL', hover=False, fg_color='#000000')
    kpopTagTemp.deselect()
    kpopTagTemp.grid(row=0, column=3 , sticky='w')
    #second row
    explicitVarTemp = tk.StringVar()
    explicitTagTemp = CTkCheckBox(tagsTemp, text="explicit", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=explicitVarTemp, onvalue='explicit', offvalue='NULL', hover=False, fg_color='#000000')
    explicitTagTemp.deselect()
    explicitTagTemp.grid(row=1, column=0, sticky='w')
    inhouseVarTemp = tk.StringVar()
    inhouseTagTemp = CTkCheckBox(tagsTemp, text="inhouse", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=inhouseVarTemp, onvalue='inhouse', offvalue='NULL', hover=False, fg_color='#000000')
    inhouseTagTemp.deselect()
    inhouseTagTemp.grid(row=1, column=1, sticky='w')
    lofiVarTemp = tk.StringVar()
    lofiTagTemp = CTkCheckBox(tagsTemp, text="lofi", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=lofiVarTemp, onvalue='lofi', offvalue='NULL', hover=False, fg_color='#000000')
    lofiTagTemp.deselect()
    lofiTagTemp.grid(row=1, column=2, sticky='w')
    if popVarTempValue != 'None':
        popTagTemp.select()
    if hiphopVarTempValue != 'None':
        hiphopTagTemp.select()
    if indieVarTempValue != 'None':
        indieTagTemp.select()
    if kpopVarTempValue != 'None':
        kpopTagTemp.select()
    if explicitVarTempValue != 'None':
        explicitTagTemp.select()
    if inhouseVarTempValue != 'None':
        inhouseTagTemp.select()
    if lofiVarTempValue != 'None':
        lofiTagTemp.select()
    # it will check which tags were selected before and only select them
    popTagTemp.configure(state=tk.DISABLED)
    hiphopTagTemp.configure(state=tk.DISABLED)
    indieTagTemp.configure(state=tk.DISABLED)
    kpopTagTemp.configure(state=tk.DISABLED)
    explicitTagTemp.configure(state=tk.DISABLED)
    inhouseTagTemp.configure(state=tk.DISABLED)
    lofiTagTemp.configure(state=tk.DISABLED)
    def saveFile(initialDirectory):
        if os.path.exists(initialDirectory):
            destinationDirectory = filedialog.askdirectory()
            initialDirectory = initialDirectory.split("/")[-1]
            destinationFilePath = os.path.join(destinationDirectory, initialDirectory)
            initialDirectory = os.path.join('databasefiles/', initialDirectory)
            shutil.copy(initialDirectory, destinationFilePath)
            # if a user requests to save the song file or the image file when on this page, it will copy that file from the databasefiles directory and copy it to
            # where the user wants it to be
        else:
            messagebox.showwarning('internal error', 'it seems that the original file has been deleted from the databasefiles folder. check your recycle bin or cloud saves to retrieve it')
    tagsTemp.grid(row=1, column=0, sticky='w', pady=(15,0))
    importsGridTemp = tk.Label(splitGridTemp, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='left')
    ##
    importArtworkImageTemp = tk.Label(importsGridTemp, image=newPhotoTemp, anchor='c', bg='#FFFFFF',fg='#B0B0B0', relief='solid', borderwidth=1, activebackground='#FFFFFF',activeforeground='#B0B0B0', justify=tk.CENTER)
    importArtworkImageTemp.grid(row=0, column=0, sticky='news', padx=(0,20))
    importsGridInsideTemp = tk.Label(importsGridTemp, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='right')
    ##
    importSongTemp = tk.Label(importsGridInsideTemp, text=songShortenedLocationTemp, font='"Space Grotesk" 13', anchor='sw', bg='#FFFFFF',fg='#B0B0B0', relief='solid', borderwidth=1, activebackground='#FFFFFF',activeforeground='#B0B0B0',  justify=tk.LEFT, height=3, wraplength=210)
    importSongTemp.grid(row=0,column=0, sticky='news', pady=(0,18))
    importSongTemp.image = songShortenedLocationTemp
    ##
    addMiscFilesTemp = tk.Button(importsGridInsideTemp, text=addMiscFilesTempValueShortened, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=21, fg='#B0B0B0', bg='#FFFFFF', activebackground='#FFFFFF',activeforeground='#B0B0B0', justify=tk.LEFT, anchor='w', cursor='hand2', command=lambda: webbrowser.open(addMiscFilesTempValue))
    addMiscFilesTemp.grid(row=1,column=0, sticky = "nsew")  
    importsGridInsideTemp.grid(row=0, column=1, padx=(10,0), sticky='e')
    importsGridTemp.grid(row=2, column=0, sticky='w', pady=(20,0), rowspan=3)

    downloadImage = Image.open('download image.png')
    resizedDownloadImage = downloadImage.resize((60,17))
    resizedDownloadImagePhotoImage = ImageTk.PhotoImage(resizedDownloadImage)
    downloadSong = Image.open('download song.png')
    resizedDownloadSong = downloadSong.resize((50,17))
    resizedDownloadSongPhotoImage = ImageTk.PhotoImage(resizedDownloadSong)

    imageAndSongGridTemp = tk.Label(splitGridTemp, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='left')

    downloadArtworkButton = tk.Button(imageAndSongGridTemp, image=resizedDownloadImagePhotoImage, anchor='nw', bg='#FFFFFF',fg='#B0B0B0', relief='flat', borderwidth=0, activebackground='#FFFFFF',activeforeground='#B0B0B0', cursor='hand2', justify=tk.LEFT, command=lambda:saveFile(ArtworkImageLocationTempValue))
    downloadArtworkButton.grid(row=0, column=0, sticky='w', padx=(0,105))
    downloadArtworkButton.image = resizedDownloadImagePhotoImage

    downloadSongButton = tk.Button(imageAndSongGridTemp, image=resizedDownloadSongPhotoImage, anchor='nw', bg='#FFFFFF',fg='#B0B0B0', relief='flat', borderwidth=0, activebackground='#FFFFFF',activeforeground='#B0B0B0', cursor='hand2', justify=tk.LEFT, command=lambda:saveFile(importSongTempValue))
    downloadSongButton.grid(row=0, column=1, sticky='w', padx=5)
    downloadSongButton.image = resizedDownloadSongPhotoImage
    imageAndSongGridTemp.grid(row=5, column=0, sticky='news', pady=10)
    #col2
    releaseDateTemp = tk.Label(splitGridTemp, text=releaseDateTempValue, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=38, fg='#B0B0B0', bg='#FFFFFF', justify=tk.LEFT, anchor='w')
    releaseDateTemp.grid(row=0,column=1, sticky = "nsew")
    performedByTemp = tk.Label(splitGridTemp, text=performedByTempValue, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=38, fg='#B0B0B0', bg='#FFFFFF', justify=tk.LEFT, anchor='w')
    performedByTemp.grid(row=2,column=1, sticky = "nsew", pady=(20,0))
    writtenByTemp = tk.Label(splitGridTemp, text=writtenByTempValue, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=38, fg='#B0B0B0', bg='#FFFFFF', justify=tk.LEFT, anchor='w')
    writtenByTemp.grid(row=3,column=1, sticky = "nsew", pady=(15,0))
    prodByTemp = tk.Label(splitGridTemp, text=prodByTempValue, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=38, fg='#B0B0B0', bg='#FFFFFF', justify=tk.LEFT, anchor='w')
    prodByTemp.grid(row=4,column=1, sticky = "nsew", pady=(15,0))

    splitGridTemp.grid(row=1, column=0, sticky='ew')

window.mainloop()
# window.mainloop runs the tkinter program in an infinite loop unless the user presses close