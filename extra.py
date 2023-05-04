def deleteEntry(recievedData, analyticsPresent):
        
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
            addTrackingButton.destroy()
            

            if analyticsPresent == True:
                youtubeAnalytics.destroy()
                spotifyAnalytics.destroy()
                analyticsPresent = False
                
            addValuesToDB()
            print('refreshing at delete entry')
    def createCommandForDelete(recievedData, analyticsPresent):
        return lambda: deleteEntry(recievedData, analyticsPresent)








if youtubeLinkFetch != None:
                print('youtubelinkfetch', youtubeLinkFetch)
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
                
                youtubeViewCount = int(youtubeViewCount)
                totalYoutubeCount = totalYoutubeCount + youtubeViewCount

                youtubeViewCount = "{:,}".format(youtubeViewCount)

                
                spotifyTrackId = spotifyLinkFetch.find("/track/") + len("/track/")
                spotifyTrackId = spotifyLinkFetch[spotifyTrackId:spotifyTrackId+22]



                spotifyTrackInfo = sp.track(spotifyTrackId)
                spotifySongPopularity = spotifyTrackInfo['popularity']


                addTrackingButton = tk.Label(previousReleases, font='"Space Grotesk" 11', bg='#FFFFFF', padx=14, pady=0, borderwidth=0, relief='flat', width=12, height=3, text='')

                youtubeAnalytics = tk.Button(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=15, pady=5, borderwidth=0, relief='flat', foreground='#FE0404', text=youtubeViewCount, command=createCommandForYoutubeButton(youtubeLinkFetch), cursor='hand2', width=5)
                youtubeAnalytics.grid(row=0, column=0, pady=(0,3))

                spotifyAnalytics = tk.Button(addTrackingButton, font='"Space Grotesk" 11', anchor='w', bg='#FFFFFF', padx=15, pady=5, borderwidth=0, relief='flat', foreground='#1DD05D', text=spotifySongPopularity, command=createCommandForSpotifyButton(spotifyLinkFetch), cursor='hand2', width=5)
                spotifyAnalytics.grid(row=0, column=1, pady=(0,3))

                addTrackingButton.grid(row=i+1, column=1, sticky='w', columnspan=2, padx=(20,0), pady=(0,3))
                analyticsPresent = True

                deleteButton = tk.Button(previousReleases, image=resizedDeleteImagePhotoImage, cursor='hand2', relief='solid', borderwidth=1, background='#FFFFFF', activebackground='#FFFFFF', command=createCommandForDelete(fetchEntry, analyticsPresent), width=29, height=29)
                deleteButton.image = resizedDeleteImagePhotoImage
                deleteButton.grid(row=i+1, column=3, sticky='w', padx=(20,10), pady=(0,3))
                print('im doing the first cmd')