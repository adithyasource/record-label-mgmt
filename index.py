import tkinter as tk
from tkinter import messagebox
import sqlite3

# app frame
window = tk.Tk()
window.title('MIMIC Internal Mgmt')
window.geometry('1000x450')
window.resizable(False, False)
window.iconbitmap('C:\\Users\\getsg\\Documents\\GitHub\\music mgmt\\mimic.ico')
window.configure(bg='#FFFFFF')
frame = tk.Frame(window, bg='#FFFFFF')
frame2 = tk.Frame(window, bg='#FFFFFF')

for page in (frame, frame2):
    page.grid(row=0, column=0, sticky='nsew', padx=75, pady=7)



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
    error = False

    if songTitleValue == "song title":
        error = True
    if releaseDate == "release date YYYY/MM/DD":
        error = True
    if performedByValue == 'performed by':
        error = True
    if writtenByValue == 'written by':
        error = True
    if prodByValue == 'produced by':
        error = True




    if error == True:
        messagebox.showerror('internal error', 'update default values for text')
    elif error == False:
        
        conn = sqlite3.connect('data.db')
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
            lofiTag TEXT
        )
        '''
        conn.execute(tableCreateQuery)


        dataInsertQuery = '''
            INSERT INTO releaseData VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        '''.format(songTitleValue, releaseDateSQLVersion, performedByValue, writtenByValue, prodByValue, popVarValue, hiphopVarValue, indieVarValue, kpopVarValue, explicitVarValue, inhouseVarValue, lofiVarValue)
      
        cursor = conn.cursor()
        cursor.execute(dataInsertQuery, {':null':None})
        conn.commit()
        conn.close()


        #savedata
        print(songTitleValue)
        print(releaseDateValue)
        print(performedByValue)
        print(writtenByValue)
        print(prodByValue)

        print(popVarValue)
        print(hiphopVarValue)
        print(indieVarValue)
        print(explicitVarValue)
        print(kpopVarValue)
        print(inhouseVarValue)
        print(lofiVarValue)
        
        songTitle.delete(0, tk.END)
        songTitle.insert(0, 'song title')

        releaseDate.delete(0, tk.END)
        releaseDate.insert(0, 'release date YYYY/MM/DD')

        performedBy.delete(0, tk.END)
        performedBy.insert(0, 'performed by')

        writtenBy.delete(0, tk.END)
        writtenBy.insert(0, 'written by')

        prodBy.delete(0, tk.END)
        prodBy.insert(0, 'produced by')

        popTag.deselect()
        hiphopTag.deselect()
        indieTag.deselect()
        explicitTag.deselect()
        kpopTag.deselect()
        inhouseTag.deselect()
        lofiTag.deselect()

        frame.tkraise()

    
    



# PAGE 1 

logo = tk.PhotoImage(file='C:\\Users\\getsg\\Documents\\GitHub\\music mgmt\\mimic logo full.png')
topLabel = tk.Label(frame, image=logo, anchor='w', bg='#FFFFFF')
topLabel.grid(row=0, column=0, pady=(30,10), sticky = "ew", )



createRelease = tk.Button(frame, text="create release", font='"Space Grotesk" 13', width=80, anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, command=lambda: showPage(frame2))
createRelease.grid(row=1, column=0, pady=10, sticky = "ew")


previousReleases = tk.Label(frame, bg='#FFFFFF',  borderwidth=1, relief='solid')
previousReleasesText = tk.Label(previousReleases, text='previous releases', font='"Space Grotesk" 13', anchor='w', padx=20, bg='#FFFFFF', foreground='#B0B0B0', pady=5)
previousReleasesText.grid(row=0,column=0, sticky = "ew")  

entry1 = tk.Label(previousReleases, text='', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
entry1.grid(row=1,column=0, sticky = "ew")  
entry2 = tk.Label(previousReleases, text='', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
entry2.grid(row=2,column=0, sticky = "ew")
entry3 = tk.Label(previousReleases, text='', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
entry3.grid(row=3,column=0, sticky = "ew")
entry4 = tk.Label(previousReleases, text='', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
entry4.grid(row=4,column=0, sticky = "ew")

#entry5 = tk.Label(previousReleases, text='', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
#entry5.grid(row=5,column=0, sticky = "ew")
#entry6 = tk.Label(previousReleases, text='', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
#entry6.grid(row=6,column=0, sticky = "ew")
#entry7 = tk.Label(previousReleases, text='', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
#entry7.grid(row=7,column=0, sticky = "ew")
#entry8 = tk.Label(previousReleases, text='', font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
#entry8.grid(row=8,column=0, sticky = "ew")
previousReleases.grid(row=2,column=0, sticky = "ew", pady=10)


viewAnalytics = tk.Button(frame, text="view analytics", font='"Space Grotesk" 13', anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20)
viewAnalytics.grid(row=3, column=0, pady=10, sticky = "swe")



# PAGE 2


backButton = tk.Button(frame2, text="< back", font='"Space Grotesk" 13', width=100, anchor='w', bg='#FFFFFF', relief='flat', activebackground='#FFFFFF', borderwidth=0, command=lambda: showPage(frame) )
backButton.grid(row=0, column=0, pady=30)

splitGrid = tk.Label(frame2, bg='#FFFFFF',  borderwidth=0, relief='flat')

#col1


songTitle = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
songTitle.grid(row=1,column=0, sticky = "nsew", padx=(0,50))  
songTitle.insert(0, "song title")

tags = tk.Label(splitGrid, bg='#FFFFFF',  borderwidth=0, relief='flat', justify='left')

#first row
popVar = tk.StringVar()
popTag = tk.Checkbutton(tags, text='pop', font='"Space Grotesk" 10', bg='#FFFFFF', activebackground='#FFFFFF', variable=popVar, onvalue='pop', offvalue='NULL')
popTag.deselect()
popTag.grid(row=0, column=0, sticky='w')

hiphopVar = tk.StringVar()
hiphopTag = tk.Checkbutton(tags, text='hip hop', font='"Space Grotesk" 10', bg='#FFFFFF', activebackground='#FFFFFF', variable=hiphopVar, onvalue='hiphop', offvalue='NULL')
hiphopTag.deselect()
hiphopTag.grid(row=0, column=1 , sticky='w')

indieVar = tk.StringVar()
indieTag = tk.Checkbutton(tags, text='indie', font='"Space Grotesk" 10', bg='#FFFFFF', activebackground='#FFFFFF', variable=indieVar, onvalue='indie', offvalue='NULL')
indieTag.deselect()
indieTag.grid(row=0, column=2 , sticky='w')

kpopVar = tk.StringVar()
kpopTag = tk.Checkbutton(tags, text='kpop', font='"Space Grotesk" 10', bg='#FFFFFF', activebackground='#FFFFFF', variable=kpopVar, onvalue='kpop', offvalue='NULL')
kpopTag.deselect()
kpopTag.grid(row=0, column=3 , sticky='w')

#second row
explicitVar = tk.StringVar()
explicitTag = tk.Checkbutton(tags, text='explicit', font='"Space Grotesk" 10', bg='#FFFFFF', activebackground='#FFFFFF', variable=explicitVar, onvalue='explicit', offvalue='NULL')
explicitTag.deselect()
explicitTag.grid(row=1, column=0, sticky='w')

inhouseVar = tk.StringVar()
inhouseTag = tk.Checkbutton(tags, text='inhouse label', font='"Space Grotesk" 10', bg='#FFFFFF', activebackground='#FFFFFF', variable=inhouseVar, onvalue='inhouse', offvalue='NULL')
inhouseTag.deselect()
inhouseTag.grid(row=1, column=1, sticky='w')

lofiVar = tk.StringVar()
lofiTag = tk.Checkbutton(tags, text='lofi', font='"Space Grotesk" 10', bg='#FFFFFF', activebackground='#FFFFFF', variable=lofiVar, onvalue='lofi', offvalue='NULL')
lofiTag.deselect()
lofiTag.grid(row=1, column=2, sticky='w')


tags.grid(row=2, column=0, sticky='w', pady=(15,0))




#col2
releaseDate = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
releaseDate.grid(row=1,column=1, sticky = "nsew")
releaseDate.insert(0, "release date YYYY/MM/DD")

performedBy = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
performedBy.grid(row=3,column=1, sticky = "nsew", pady=(15,0))
performedBy.insert(0, "performed by")

writtenBy = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
writtenBy.grid(row=4,column=1, sticky = "nsew", pady=(15,0))
writtenBy.insert(0, "written by")

prodBy = tk.Entry(splitGrid, borderwidth=1, relief='solid', font='"Space Grotesk" 13', width=35, fg='#B0B0B0')
prodBy.grid(row=5,column=1, sticky = "nsew", pady=(15,0))
prodBy.insert(0, "produced by")


saveRelease = tk.Button(splitGrid, font='"Space Grotesk" 13', bg='#FFFFFF', text='save release', relief='flat', activebackground='#FFFFFF', command=lambda: [doShit(frame)], borderwidth=0)
saveRelease.grid(row= 6, column=1, pady=(30,0), sticky='e')

splitGrid.grid(row=1, column=0, sticky='ew')


window.mainloop()