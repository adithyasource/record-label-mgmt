import tkinter as tk
from tkinter import messagebox
import sqlite3
import itertools
import customtkinter


# app frame
window = tk.Tk()
window.title('MIMIC Internal Mgmt')
window.geometry('1000x450')
window.resizable(False, True)
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

        # if popVarValue == "NULL":
        #     popVarValue = None
        # if hiphopVarValue == "NULL":
        #     hiphopVarValue = None
        # if indieVarValue == "NULL":
        #     indieVarValue = None
        # if kpopVarValue == "NULL":
        #     kpopVarValue = None
        # if explicitVarValue == "NULL":
        #     explicitVarValue = None
        # if inhouseVarValue == "NULL":
        #     inhouseVarValue = None
        # if lofiVarValue == "NULL":
        #     lofiVarValue = None

        dataInsertQuery = '''
            INSERT INTO releaseData VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
        '''.format(songTitleValue, releaseDateValue, performedByValue, writtenByValue, prodByValue, popVarValue, hiphopVarValue, indieVarValue, kpopVarValue, explicitVarValue, inhouseVarValue, lofiVarValue)
      
        cursor = conn.cursor()
        cursor.execute(dataInsertQuery)
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



createRelease = tk.Button(frame, text="create release", font='"Space Grotesk" 13', width=80, anchor='w', bg='#FFFFFF', relief='solid', borderwidth=1, activebackground='#FFFFFF', padx=20, command=lambda: showPage(frame2), cursor='hand2')
createRelease.grid(row=1, column=0, pady=10, sticky = "ew")






previousReleases = tk.Frame(frame, bg='#FFFFFF',  borderwidth=1, relief='solid', width=100)

previousReleasesText = tk.Label(previousReleases, text='previous releases', font='"Space Grotesk" 13', anchor='w', padx=20, bg='#FFFFFF', foreground='#B0B0B0', pady=5)
previousReleasesText.grid(row=0,column=0, sticky = "ew")  


conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute("SELECT songTitle from releaseData")
fetchAllEntries = cursor.fetchall()
numberOfEntries = len(fetchAllEntries)

for i in range(numberOfEntries):
    globals()[f'fetchEntry{i+1}'] = fetchAllEntries[i]
    globals()[f'fetchEntry{i+1}'] = str(globals()[f'fetchEntry{i+1}'])[2:-3]
    globals()[f'entry{i+1}'] = tk.Label(previousReleases, text=globals()[f'fetchEntry{i+1}'], font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=20, pady=5)
    globals()[f'entry{i+1}'].grid(row=i+1,column=0, sticky = "ew") 
conn.commit()
conn.close()

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
popTag = customtkinter.CTkCheckBox(tags, text="pop", font=customtkinter.CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=popVar, onvalue='pop', offvalue='NULL', hover=False, fg_color='#000000')
popTag.deselect()
popTag.grid(row=0, column=0, sticky='w')

hiphopVar = tk.StringVar()
hiphopTag = customtkinter.CTkCheckBox(tags, text="hip hop", font=customtkinter.CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=hiphopVar, onvalue='hiphop', offvalue='NULL', hover=False, fg_color='#000000')
hiphopTag.deselect()
hiphopTag.grid(row=0, column=1 , sticky='w')

indieVar = tk.StringVar()
indieTag = customtkinter.CTkCheckBox(tags, text="indie", font=customtkinter.CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=indieVar, onvalue='indie', offvalue='NULL', hover=False, fg_color='#000000')
indieTag.deselect()
indieTag.grid(row=0, column=2 , sticky='w')

kpopVar = tk.StringVar()
kpopTag = customtkinter.CTkCheckBox(tags, text="kpop", font=customtkinter.CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=kpopVar, onvalue='kpop', offvalue='NULL', hover=False, fg_color='#000000')
kpopTag.deselect()
kpopTag.grid(row=0, column=3 , sticky='w')

#second row
explicitVar = tk.StringVar()
explicitTag = customtkinter.CTkCheckBox(tags, text="explicit", font=customtkinter.CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=explicitVar, onvalue='explicit', offvalue='NULL', hover=False, fg_color='#000000')
explicitTag.deselect()
explicitTag.grid(row=1, column=0, sticky='w')

inhouseVar = tk.StringVar()
inhouseTag = customtkinter.CTkCheckBox(tags, text="inhouse", font=customtkinter.CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=inhouseVar, onvalue='inhouse', offvalue='NULL', hover=False, fg_color='#000000')
inhouseTag.deselect()
inhouseTag.grid(row=1, column=1, sticky='w')

lofiVar = tk.StringVar()
lofiTag = customtkinter.CTkCheckBox(tags, text="lofi", font=customtkinter.CTkFont(family='Space Grotesk', size=13), border_width=1, corner_radius=0, checkbox_height=20, checkbox_width=20, variable=lofiVar, onvalue='lofi', offvalue='NULL', hover=False, fg_color='#000000')
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


saveRelease = tk.Button(splitGrid, font='"Space Grotesk" 13', bg='#FFFFFF', text='save release', relief='flat', activebackground='#FFFFFF', command=lambda: [doShit(frame)], borderwidth=0, cursor='hand2')
saveRelease.grid(row= 6, column=1, pady=(30,0), sticky='e')

splitGrid.grid(row=1, column=0, sticky='ew')


window.mainloop()