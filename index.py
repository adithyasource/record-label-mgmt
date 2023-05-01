import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
from customtkinter import set_appearance_mode
from customtkinter import CTkCheckBox
from customtkinter import CTkFont

# app frame
window = tk.Tk()
window.title('MIMIC Internal Mgmt')
window.geometry('1000x450')
window.resizable(False, True)
window.iconbitmap('mimic.ico')
window.configure(bg='#FFFFFF')
frame = tk.Frame(window, bg='#FFFFFF')
frame2 = tk.Frame(window, bg='#FFFFFF')
tempFrameForEntry = tk.Frame(window, bg='#FFFFFF')
set_appearance_mode('light')
songLocation = ''


for page in (frame, frame2, tempFrameForEntry):
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
            artworkImage BLOB
        )
        '''

def askForImage():
    global getImage
    getImage = filedialog.askopenfilenames(title='select artwork', filetypes=(('png', "*.png"), ("jpg", "*.jpg")))
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
    maxLengthOfText = 20
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
        messagebox.showerror('internal error', 'include artwork')
    else:
        if isSongButtonClicked == False:
            songLocation = None
            messagebox.showerror('internal error', 'include song')
        else:
            isSongButtonClicked == True
            songLocation = str(getSong)[2:-3]
            if error == True:
                messagebox.showerror('internal error', 'update default values for text')
            elif error == False:
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
createRelease = tk.Button(frame, text="create release", font='"Space Grotesk" 13', width=80, anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, command=lambda: showPage(frame2), cursor='hand2')
createRelease.grid(row=1, column=0, pady=10, sticky = "ew")
previousReleases = tk.Frame(frame, bg='#FFFFFF',  borderwidth=1, relief='solid', width=100)
previousReleasesText = tk.Label(previousReleases, text='previous releases', font='"Space Grotesk" 13', anchor='w', padx=20, bg='#FFFFFF', foreground='#B0B0B0', pady=5)
previousReleasesText.grid(row=0,column=0, sticky = "ew")  


def addValuesToDB():
    conn = sqlite3.connect('data.db')
    conn.execute(tableCreateQuery)
    cursor = conn.cursor()
    cursor.execute("SELECT songTitle from releaseData")
    fetchAllEntries = cursor.fetchall()
    numberOfEntries = len(fetchAllEntries)

    for i in range(numberOfEntries):
        globals()[f'fetchEntry{i+1}'] = fetchAllEntries[i]
        globals()[f'fetchEntry{i+1}'] = str(globals()[f'fetchEntry{i+1}'])[2:-3]
        globals()[f'entry{i+1}'] = tk.Button(previousReleases, text=globals()[f'fetchEntry{i+1}'], font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5, borderwidth=0, width=90, cursor='hand2', command=lambda: [showEntryPage(globals()[f'fetchEntry{i+1}'])])
        globals()[f'entry{i+1}'].grid(row=i+1,column=0, sticky = "ew") 
        
    conn.commit()
    conn.close()
addValuesToDB()


previousReleases.grid(row=2,column=0, sticky = "ew", pady=10)
viewAnalytics = tk.Button(frame, text="view analytics", font='"Space Grotesk" 13', anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, cursor='hand2')
viewAnalytics.grid(row=3, column=0, pady=10, sticky = "swe")

# PAGE 2
backButton = tk.Button(frame2, text="< back", font='"Space Grotesk" 13', width=100, anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, command=lambda: showPage(frame), cursor='hand2' )
backButton.grid(row=0, column=0, pady=30)
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
importSong = tk.Button(importsGridInside, text="import song", font='"Space Grotesk" 13', anchor='sw', bg='#FFFFFF',fg='#B0B0B0', relief='solid', borderwidth=1, activebackground='#FFFFFF',activeforeground='#B0B0B0',  cursor='hand2', justify=tk.LEFT, height=3, command=askForSong)
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
saveRelease.grid(row= 6, column=1, pady=(30,0), sticky='e')
splitGrid.grid(row=1, column=0, sticky='ew')



#################
#################

def showEntryPage(lmao):

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT songTitle from releaseData")
    fetchAllEntries = cursor.fetchall()
    numberOfEntries = len(fetchAllEntries)

    for i in range(numberOfEntries):
        globals()[f'fetchEntry{i+1}'] = fetchAllEntries[i]
        globals()[f'fetchEntry{i+1}'] = str(globals()[f'fetchEntry{i+1}'])[2:-3]
        globals()[f'entry{i+1}'] = tk.Button(previousReleases, text=globals()[f'fetchEntry{i+1}'], font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5, borderwidth=0, width=90, cursor='hand2', command=lambda: [showEntryPage(globals()[f'fetchEntry{i+1}'])])
        globals()[f'entry{i+1}'].grid(row=i+1,column=0, sticky = "ew") 
        
    conn.commit()
    conn.close()


    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    selectValuesFromTable = '''SELECT * FROM releaseData WHERE songTitle = ?'''
    cursor.execute(selectValuesFromTable, (str(lmao),))



    
    fetchAllEntries = cursor.fetchall()

    conn.commit()

    conn.close()

    songTitleTempValue, releaseDateTempValue, performedByTempValue, writtenByTempValue, prodByTempValue, popVarTempValue, hiphopVarTempValue, indieVarTempValue, kpopVarTempValue, explicitVarTempValue, inhouseVarTempValue, lofiVarTempValue, ArtworkImageLocationTempValue, importSongTempValue, addMiscFilesTempValue, importArtworkImageTempValue = fetchAllEntries[0]

    print(songTitleTempValue)

    tempFrameForEntry.tkraise()
    backButtonTemp = tk.Button(tempFrameForEntry, text="< back", font='"Space Grotesk" 13', width=100, anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, cursor='hand2', command=lambda: showPage(frame))
    backButtonTemp.grid(row=0, column=0, pady=30)
    splitGridTemp = tk.Label(tempFrameForEntry, bg='#FFFFFF',  borderwidth=0, relief='flat')
    #col1
    songTitleTemp = tk.Label(splitGridTemp, text=songTitleTempValue, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
    songTitleTemp.grid(row=1,column=0, sticky = "nsew", padx=(0,50))  
    tagsTemp = tk.Label(splitGridTemp, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='left')
    #first row
    popVarTemp = tk.StringVar()
    popTagTemp = CTkCheckBox(tagsTemp, text="pop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=popVar, onvalue='pop', offvalue='NULL', hover=False, fg_color='#000000')
    popTagTemp.deselect()
    popTagTemp.grid(row=0, column=0, sticky='w')
    hiphopVarTemp = tk.StringVar()
    hiphopTagTemp = CTkCheckBox(tagsTemp, text="hip hop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=hiphopVar, onvalue='hiphop', offvalue='NULL', hover=False, fg_color='#000000')
    hiphopTagTemp.deselect()
    hiphopTagTemp.grid(row=0, column=1 , sticky='w')
    indieVarTemp = tk.StringVar()
    indieTagTemp = CTkCheckBox(tagsTemp, text="indie", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=indieVar, onvalue='indie', offvalue='NULL', hover=False, fg_color='#000000')
    indieTagTemp.deselect()
    indieTagTemp.grid(row=0, column=2 , sticky='w')
    kpopVarTemp = tk.StringVar()
    kpopTagTemp = CTkCheckBox(tagsTemp, text="kpop", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=kpopVar, onvalue='kpop', offvalue='NULL', hover=False, fg_color='#000000')
    kpopTagTemp.deselect()
    kpopTagTemp.grid(row=0, column=3 , sticky='w')
    #second row
    explicitVarTemp = tk.StringVar()
    explicitTagTemp = CTkCheckBox(tagsTemp, text="explicit", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=explicitVar, onvalue='explicit', offvalue='NULL', hover=False, fg_color='#000000')
    explicitTagTemp.deselect()
    explicitTagTemp.grid(row=1, column=0, sticky='w')
    inhouseVarTemp = tk.StringVar()
    inhouseTagTemp = CTkCheckBox(tagsTemp, text="inhouse", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=inhouseVar, onvalue='inhouse', offvalue='NULL', hover=False, fg_color='#000000')
    inhouseTagTemp.deselect()
    inhouseTagTemp.grid(row=1, column=1, sticky='w')
    lofiVarTemp = tk.StringVar()
    lofiTagTemp = CTkCheckBox(tagsTemp, text="lofi", font=CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=lofiVar, onvalue='lofi', offvalue='NULL', hover=False, fg_color='#000000')
    lofiTagTemp.deselect()
    lofiTagTemp.grid(row=1, column=2, sticky='w')
    tagsTemp.grid(row=2, column=0, sticky='w', pady=(15,0))
    importsGridTemp = tk.Label(splitGridTemp, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='left')
    ##
    importArtworkImageTemp = tk.Button(importsGridTemp, text="import artwork", font='"Space Grotesk" 13', anchor='sw', bg='#FFFFFF',fg='#B0B0B0', relief='solid', borderwidth=1, activebackground='#FFFFFF',activeforeground='#B0B0B0', cursor='hand2', justify=tk.LEFT,)
    importArtworkImageTemp.grid(row=0, column=0, sticky='news', padx=(0,20))
    importsGridInsideTemp = tk.Label(importsGridTemp, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='right')
    ##
    importSongTemp = tk.Button(importsGridInsideTemp, text="import song", font='"Space Grotesk" 13', anchor='sw', bg='#FFFFFF',fg='#B0B0B0', relief='solid', borderwidth=1, activebackground='#FFFFFF',activeforeground='#B0B0B0',  cursor='hand2', justify=tk.LEFT, height=3)
    importSongTemp.grid(row=0,column=0, sticky='news', pady=(0,19))
    ##
    addMiscFilesTemp = tk.Entry(importsGridInsideTemp, borderwidth=1, relief='solid', font='"Space Grotesk" 13', fg='#B0B0B0')
    addMiscFilesTemp.grid(row=1,column=0, sticky = "nsew")  
    addMiscFilesTemp.insert(0, "link to misc files")
    importsGridInsideTemp.grid(row=0, column=1, padx=(10,0), sticky='e')
    importsGridTemp.grid(row=3, column=0, sticky='w', pady=(20,0), rowspan=3)

    #col2
    releaseDateTemp = tk.Entry(splitGridTemp, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
    releaseDateTemp.grid(row=1,column=1, sticky = "nsew")
    releaseDateTemp.insert(0, "release date yyyy/mm/dd")
    performedByTemp = tk.Entry(splitGridTemp, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
    performedByTemp.grid(row=3,column=1, sticky = "nsew", pady=(20,0))
    performedByTemp.insert(0, "performed by")
    writtenByTemp = tk.Entry(splitGridTemp, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
    writtenByTemp.grid(row=4,column=1, sticky = "nsew", pady=(15,0))
    writtenByTemp.insert(0, "written by")
    prodByTemp = tk.Entry(splitGridTemp, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
    prodByTemp.grid(row=5,column=1, sticky = "nsew", pady=(15,0))
    prodByTemp.insert(0, "produced by")

    saveReleaseTemp = tk.Button(splitGridTemp, font='"Space Grotesk" 13', bg='#FFFFFF', text='save release', relief='flat', activebackground='#FFFFFF', borderwidth=0, cursor='hand2')
    saveReleaseTemp.grid(row= 6, column=1, pady=(30,0), sticky='e')
    splitGridTemp.grid(row=1, column=0, sticky='ew')

    







window.mainloop()