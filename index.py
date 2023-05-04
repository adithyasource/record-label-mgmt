import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
from customtkinter import set_appearance_mode
from customtkinter import CTkCheckBox
from customtkinter import CTkFont
import io
import shutil
import os
import webbrowser

window = tk.Tk()
window.title('MIMIC Internal Mgmt')
window.geometry('985x450')
window.resizable(False, True)
window.iconbitmap('mimic.ico')
window.configure(bg='#FFFFFF')
frame = tk.Frame(window, bg='#FFFFFF')
frame2 = tk.Frame(window, bg='#FFFFFF')
tempFrameForEntry = tk.Frame(window, bg='#FFFFFF')
frameForTracking = tk.Frame(window, bg='#FFFFFF')
set_appearance_mode('light')
songLocation = ''

for page in (frame, frame2, tempFrameForEntry, frameForTracking):
    page.grid(row=0, column=0, sticky='nsew', padx=75, pady=7)

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

def askForImage():
    global getImage
    while True:
        getImage = filedialog.askopenfilenames(title='select artwork', filetypes=(('png', "*.png"), ("jpg", "*.jpg")))
        if getImage:
            break
    global imageLocation
    imageLocation = str(getImage)[2:-3]

    if getImage:
        # create PhotoImage from image file
        global photo
        photo = Image.open(getImage[0])

        resizedPhoto = photo.resize((140, 140))

        newPhoto = ImageTk.PhotoImage(resizedPhoto)

        # delete previous content and insert image
        importArtworkImage.image = newPhoto

        importArtworkImage.config(text='', image=newPhoto)
        global isImageButtonClicked
        isImageButtonClicked = True

isSongButtonClicked = False
isImageButtonClicked = False

def askForSong():
    global getSong
    while True:
        getSong = filedialog.askopenfilenames(title='select song', filetypes=(('mp3', "*.mp3"), ("wav", "*.wav")))
        if getSong:  # check if user selected at least one file
            break    # exit loop if user made a selection
    global songLocation
    maxLengthOfText = 45
    songLocation = str(getSong)[2:-3]
    global isSongButtonClicked
    isSongButtonClicked = True

    shortenedLocation = songLocation[:maxLengthOfText] + "..." if len(songLocation) > maxLengthOfText else songLocation



    importSong.config(text=shortenedLocation)

def convertImageIntoBinary(photo):
    with open(photo, 'rb') as file:
        PhotoImage = file.read() 
    return PhotoImage

def showPage(frame):
    frame.tkraise()

showPage(frame)

def doShit(frame):
    #reading values
    
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

    global songLocation
    global getSong
    global isSongButtonClicked
    global isImageButtonClicked

    if isImageButtonClicked == False:
        messagebox.showwarning('internal error', 'include artwork')
    else:
        if isSongButtonClicked == False:
            songLocation = None
            messagebox.showwarning('internal error', 'include song')
        else:
            isSongButtonClicked == True
            songLocation = str(getSong)[2:-3]
            if error == True:
                messagebox.showwarning('internal error', 'update default values for text')
                
            else:
                if not miscFilesText.startswith('https://'):
                    messagebox.showwarning('internal error', 'misc files should be uploaded to a cloud drive and the web address should be stored')
                else:
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
                    frame.tkraise()
                    importSong.config(text='import song')
    
    

# PAGE 1 
logo = tk.PhotoImage(file='mimic logo full.png')
topLabel = tk.Label(frame, image=logo, anchor='w', bg='#FFFFFF')
topLabel.grid(row=0, column=0, pady=(30,10), sticky = "ew", )
createRelease = tk.Button(frame, text="create release", font='"Space Grotesk" 13', width=78, anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, command=lambda: showPage(frame2), cursor='hand2')
createRelease.grid(row=1, column=0, pady=10, sticky = "ew")
previousReleases = tk.Frame(frame, bg='#FFFFFF',  borderwidth=1, relief='solid', width=78)
previousReleasesText = tk.Label(previousReleases, text='previous releases', font='"Space Grotesk" 13', anchor='w', padx=20, bg='#FFFFFF', foreground='#B0B0B0', pady=5)
previousReleasesText.grid(row=0,column=0, sticky = "ew")  

deleteImage = Image.open('delete button.png')
resizedDeleteImage = deleteImage.resize((17,17))
#
resizedDeleteImagePhotoImage = ImageTk.PhotoImage(resizedDeleteImage)

def saveTracking(recievedData, trackYoutubeEntry, trackSpotifyEntry):
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
    
    if errorTracking == True:
        messagebox.showwarning('internal error', 'links should be in proper format, for ex \n\nyoutube\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ\n\nspotify\nhttps://open.spotify.com/track/4PTG3Z6ehGkBFwjyb...')
    else:
        conn = sqlite3.connect('data.db')


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


def addValuesToDB():
    conn = sqlite3.connect('data.db')
    conn.execute(tableCreateQuery)
    cursor = conn.cursor()
    cursor.execute("SELECT songTitle from releaseData")
    fetchAllEntries = cursor.fetchall()
    conn.commit()
    numberOfEntries = len(fetchAllEntries)
    

    def createCommandForOpen(entry):
        return lambda: showEntryPage(entry)

    def createCommandForDelete(entry):
<<<<<<< HEAD
        return deleteEntry(entry)

=======
        return lambda: deleteEntry(entry)
>>>>>>> parent of 94b8fa5 (i think its working)

    def createCommandForTracking(entry):
        return addTrackingForEntry(entry)

    def createCommandForSavingTracking(recievedData, trackYoutubeEntry, trackSpotifyEntry):
        return lambda: saveTracking(recievedData, trackYoutubeEntry, trackSpotifyEntry)

    def deleteEntry(recievedData):
        deleteReleaseQuestion = tk.messagebox.askquestion('delete release', 'you sure you want to delete this release?', icon='warning')
        if deleteReleaseQuestion == 'yes':
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            deleteValuesFromTable = '''DELETE FROM releaseData WHERE songTitle = ?'''
            cursor.execute(deleteValuesFromTable, (str(recievedData),))
            conn.commit()
            conn.close()
            entry.destroy()
            deleteButton.destroy()
<<<<<<< HEAD

            youtubeAnalytics.destroy()
            spotifyAnalytics.destroy()
=======
>>>>>>> parent of 94b8fa5 (i think its working)
            addTrackingButton.destroy()
            addValuesToDB()


    def addTrackingForEntry(recievedData):
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

<<<<<<< HEAD

    entry = tk.Label(previousReleases, text='there are no releases at the moment', font='"Space Grotesk" 13', anchor='w', padx=20, bg='#FFFFFF', foreground='#000000', pady=5)
    entry.grid(row=1,column=0, sticky = "ew")

    addTrackingButton = tk.Label(previousReleases, font='"Space Grotesk" 11', bg='#FFFFFF', padx=14, pady=0, borderwidth=0, relief='flat', width=12, height=2, text='')
        

    youtubeAnalytics = tk.Button(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=15, pady=5, borderwidth=0, relief='flat', foreground='#FE0404', width=5, text='')
    youtubeAnalytics.grid(row=0, column=0, pady=(0,3))

    spotifyAnalytics = tk.Button(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=15, pady=5, borderwidth=0, relief='flat', foreground='#1DD05D', width=5, text='')
    spotifyAnalytics.grid(row=0, column=1, pady=(0,3))



    addTrackingButton.grid(row=1, column=1, sticky='w', columnspan=2, padx=(20,0))

    deleteButton = tk.Label(previousReleases, font='"Space Grotesk" 11', bg='#FFFFFF', padx=14, pady=0, borderwidth=0, relief='flat', width=2, height=2, text='')
    deleteButton.grid(row=1, column=3, sticky='w', padx=(20,10))

    for i in range(numberOfEntries):
        
        fetchEntry = fetchAllEntries[i]
        fetchEntry = str(fetchEntry)[2:-3]
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT youtubeLink,spotifyLink from releaseData")
        fetchTrackingLinks = cursor.fetchall()
        conn.commit()
        conn.close()
        youtubeLinkFetch = fetchTrackingLinks[i][0]
        spotifyLinkFetch = fetchTrackingLinks[i][1]
        
        if not youtubeLinkFetch == None:
        #IF THER IS A LINK
            youtubeVideoId = youtubeLinkFetch.find("?v=") + len("?v=")
            youtubeVideoId = youtubeLinkFetch[youtubeVideoId:youtubeVideoId+11]
            youtubeRequest = youtubeConnect.videos().list(
                part='statistics',
                id=youtubeVideoId
            )
            youtubeResponse = youtubeRequest.execute()
            youtubeViewCount = youtubeResponse['items'][0]['statistics']['viewCount']
            youtubeViewCount = int(youtubeViewCount)
            totalYoutubeCount = totalYoutubeCount + youtubeViewCount
            youtubeViewCount = "{:,}".format(youtubeViewCount)
            spotifyTrackId = spotifyLinkFetch.find("/track/") + len("/track/")
            spotifyTrackId = spotifyLinkFetch[spotifyTrackId:spotifyTrackId+22]
            spotifyTrackInfo = sp.track(spotifyTrackId)
            spotifySongPopularity = spotifyTrackInfo['popularity']



            entry = tk.Button(previousReleases, text=fetchEntry, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5, borderwidth=0, width=62, cursor='hand2', command=createCommandForOpen(fetchEntry))
            entry.grid(row=i+1, column=0, sticky="w", pady=(0,3))
            addTrackingButton = tk.Label(previousReleases, font='"Space Grotesk" 11', bg='#FFFFFF', padx=14, pady=0, borderwidth=0, relief='flat', width=12, height=3, text='')

            youtubeAnalytics = tk.Button(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=15, pady=5, borderwidth=0, relief='flat', foreground='#FE0404', text=youtubeViewCount, command=createCommandForYoutubeButton(youtubeLinkFetch), cursor='hand2', width=5)
            youtubeAnalytics.grid(row=0, column=0, pady=(0,3))

            spotifyAnalytics = tk.Button(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=15, pady=5, borderwidth=0, relief='flat', foreground='#1DD05D', text=spotifySongPopularity, command=createCommandForSpotifyButton(spotifyLinkFetch), cursor='hand2', width=5)
            spotifyAnalytics.grid(row=0, column=1, pady=(0,3))

            addTrackingButton.grid(row=i+1, column=1, sticky='w', columnspan=2, padx=(20,0), pady=(0,3))
            deleteButton = tk.Button(previousReleases, image=resizedDeleteImagePhotoImage, cursor='hand2', relief='solid', borderwidth=1, background='#FFFFFF', activebackground='#FFFFFF', command=lambda: createCommandForDelete(fetchEntry), width=29, height=29)
            deleteButton.image = resizedDeleteImagePhotoImage
            deleteButton.grid(row=i+1, column=3, sticky='w', padx=(20,10), pady=(0,3))
            

        else:
        #IF LINK noT THERE
            
            entry = tk.Button(previousReleases, text=fetchEntry, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5, borderwidth=0, width=62, cursor='hand2', command=createCommandForOpen(fetchEntry))
            entry.grid(row=i+1, column=0, sticky="w", pady=(0,3))
    
            addTrackingButton = tk.Button(previousReleases, text='add tracking', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=14, pady=0, borderwidth=1, cursor='hand2', relief='solid', command=lambda:createCommandForTracking(fetchEntry), activebackground='#FFFFFF')
            
            
            addTrackingButton.grid(row=i+1, column=1, sticky='w', columnspan=2, padx=(20,0), pady=(0,3))

            deleteButton = tk.Button(previousReleases, image=resizedDeleteImagePhotoImage, cursor='hand2', relief='solid', borderwidth=1, background='#FFFFFF', activebackground='#FFFFFF', command=lambda: createCommandForDelete(fetchEntry), width=29, height=29)
            deleteButton.image = resizedDeleteImagePhotoImage
            deleteButton.grid(row=i+1, column=3, sticky='w', padx=(20,10), pady=(0,3))
    print(totalYoutubeCount)
=======
    if numberOfEntries == 0:
        noReleasesText = tk.Label(previousReleases, text='there are no releases at the moment', font='"Space Grotesk" 13', anchor='w', padx=20, bg='#FFFFFF', foreground='#000000', pady=5)
        noReleasesText.grid(row=1,column=0, sticky = "ew")  
        addTrackingButton = tk.Label(text='', background='#FFFFFF', foreground='#FFFFFF')
        deleteButton = tk.Label(text='', background='#FFFFFF', foreground='#FFFFFF')
    else:
        for i in range(numberOfEntries):
            fetchEntry = fetchAllEntries[i]
            fetchEntry = str(fetchEntry)[2:-3]
            entry = tk.Button(previousReleases, text=fetchEntry, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5, borderwidth=0, width=62, cursor='hand2', command=createCommandForOpen(fetchEntry))
            entry.grid(row=i+1, column=0, sticky="w", pady=(0,3))
            cursor.execute("SELECT youtubeLink,spotifyLink from releaseData")
            fetchTrackingLinks = cursor.fetchall()
            conn.commit()
            link1 = fetchTrackingLinks[i][0]
            if link1 != None:
                addTrackingButton = tk.LabelFrame(previousReleases, font='"Space Grotesk" 11', bg='#FFFFFF', padx=14, pady=0, borderwidth=0, relief='flat', width=12, height=2)

                youtubeAnalytics = tk.Label(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=14, pady=0, borderwidth=0, relief='flat', foreground='#FE0404')
                youtubeAnalytics.grid(row=0, column=0)

                spotifyAnalytics = tk.Label(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=14, pady=0, borderwidth=0, relief='flat', foreground='#1DD05D')
                spotifyAnalytics.grid(row=0, column=1)

                addTrackingButton.grid(row=i+1, column=1, sticky='w', columnspan=2, padx=(20,0), pady=(0,3))
            else:
                addTrackingButton = tk.Button(previousReleases, text='add tracking', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=14, pady=0, borderwidth=1, cursor='hand2', relief='solid', command=createCommandForTracking(fetchEntry))
                addTrackingButton.grid(row=i+1, column=1, sticky='w', columnspan=2, padx=(20,0), pady=(0,3))
            
            deleteButton = tk.Button(previousReleases, image=resizedDeleteImagePhotoImage, cursor='hand2', relief='solid', borderwidth=1, background='#FFFFFF', activebackground='#FFFFFF', command=createCommandForDelete(fetchEntry), width=29, height=29)
            deleteButton.image = resizedDeleteImagePhotoImage
            deleteButton.grid(row=i+1, column=3, sticky='w', padx=(20,10), pady=(0,3))
        
    conn.close()
>>>>>>> parent of 94b8fa5 (i think its working)

addValuesToDB()





previousReleases.grid(row=2,column=0, sticky = "ew", pady=10)

<<<<<<< HEAD


=======
viewAnalytics = tk.Button(frame, text="view analytics", font='"Space Grotesk" 13', anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, cursor='hand2')
viewAnalytics.grid(row=3, column=0, pady=10, sticky = "swe")
>>>>>>> parent of 94b8fa5 (i think its working)




# PAGE 2
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

saveRelease = tk.Button(splitGrid, font='"Space Grotesk" 13', bg='#FFFFFF', text='save release', relief='flat', activebackground='#FFFFFF', command=lambda: [doShit(frame), convertImageIntoBinary(photo)], borderwidth=0, cursor='hand2')
saveRelease.grid(row= 6, column=1, pady=(20,0), sticky='e')
splitGrid.grid(row=1, column=0, sticky='ew')



#################
#################

def showEntryPage(recievedData):

    

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    selectValuesFromTable = '''SELECT * FROM releaseData WHERE songTitle = ?'''
    cursor.execute(selectValuesFromTable, (str(recievedData),))

    fetchAllEntries = cursor.fetchall()

    conn.commit()

    conn.close()

    songTitleTempValue, releaseDateTempValue, performedByTempValue, writtenByTempValue, prodByTempValue, popVarTempValue, hiphopVarTempValue, indieVarTempValue, kpopVarTempValue, explicitVarTempValue, inhouseVarTempValue, lofiVarTempValue, ArtworkImageLocationTempValue, importSongTempValue, addMiscFilesTempValue, importArtworkImageTempValue, youtubeLinkTemp, spotifyLinkTemp = fetchAllEntries[0]
    # photoTemp = Image.frombytes("RGBA", (140,140), importArtworkImageTempValue)

    # resizedPhotoTemp = photoTemp.resize((140, 140))
    # global newPhotoTemp
    # newPhotoTemp = ImageTk.PhotoImage(resizedPhotoTemp)
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

            fileName = os.path.basename(initialDirectory)
            
            destinationFilePath = os.path.join(destinationDirectory, fileName)
            
            shutil.copy(initialDirectory, destinationFilePath)
        else:
            messagebox.showwarning('internal error', 'it seems that the original file has been deleted from your pc. check your recycle bin or cloud saves to retrieve it')

           

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


<<<<<<< HEAD

viewAnalytics = tk.Button(frame, text="view analytics", font='"Space Grotesk" 13', anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, cursor='hand2', command=lambda: showPage(frameForAnalytics))
backButton = tk.Button(frameForAnalytics, text="< back", font='"Space Grotesk" 13',  anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, command=lambda: showPage(frame), cursor='hand2', justify=tk.LEFT )
backButton.grid(row=0, column=0, pady=30, sticky='w')

firstGraph = tk.Label(frameForAnalytics, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=38, fg='#B0B0B0', bg='#FBFBFB')
firstGraph.grid(row=1,column=0, sticky = "nsew", padx=(0,50))  
secondGraph = tk.Label(frameForAnalytics, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=38, fg='#B0B0B0', bg='#FBFBFB')
secondGraph.grid(row=1,column=1, sticky = "nsew", padx=(0,40))  


viewAnalytics.grid(row=3, column=0, pady=10, sticky = "swe")


=======
>>>>>>> parent of 94b8fa5 (i think its working)
window.mainloop()