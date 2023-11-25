import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import os
import time
import ntpath #This is used to extract filename from path

from tkinter import filedialog
from pathlib import Path

from playsound import playsound
import pygame
from pygame import mixer

import ftplib
from ftplib import FTP

PORT = 8050
IP_ADDRESS = '127.0.0.1'
SERVER = None
BUFFER_SIZE = 4096

song_counter = 0
listBox = None
song_selected = None
filePathLabel = None
infoLabel = None

def downloadFile():
    # retreiving the selected song from listBox using ANCHOR
    song_to_download = listBox.get(ANCHOR)
    infoLabel.configure(text='Downloading...' + song_to_download)
    HOSTNAME = "127.0.0.1"
    USERNAME = "lftpd"
    PASSWORD = "lftpd"
    home = str(Path.home()) # getting the file path
    download_path = home + "/Downloads"
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    ftp_server.encoding = "utf-8"
    ftp_server.cwd('shared_files')
    local_filename = os.path.join(download_path, song_to_download)
    file = open(local_filename, 'wb')
    ftp_server.retrbinary('RETR ' + song_to_download, file.write)
    ftp_server.dir()
    file.close()
    ftp_server.quit()
    infoLabel.configure(text="Download Complete!")
    time.sleep(1)
    
    if song_selected != "":
        infoLabel.configure(text="Now playing: " + song_selected)
    else:
        infoLabel.configure(text="")

def browseFiles():
    global listBox
    global song_counter
    global filePathLabel

    try:
        filename = filedialog.askopenfilename()
        HOSTNAME = "127.0.0.1"
        USERNAME = "lftpd"
        PASSWORD = "lftpd"
        
        ftp_server = FTP(HOSTNAME, USERNAME, PASSWORD)
        ftp_server.encoding = "utf-8"
        ftp_server.cwd('shared_files')
        fname = ntpath.basename(filename)

        with open(filename, 'rb') as file:
            ftp_server.storbinary(f"STOR {fname}", file)
        
        ftp_server.dir()
        ftp_server.quit()

        # displaying songs in the list box
        listBox.insert(song_counter, fname) # this line adds the file to the shared text area (listBox) - super crucial!!!
        song_counter += 1
    except FileNotFoundError:
        print("Cancel button pressed")

def play():
    global song_selected
    song_selected = listBox.get(ANCHOR)
    
    pygame.mixer.init()
    # retrieves the file from the system
    pygame.mixer.music.load('shared_files/'+song_selected)
    # playing music
    pygame.mixer.music.play()

    # displaying the current song being played in the info label
    if(song_selected != ""):
        infoLabel.configure(text="Now Playing: "+song_selected)
    else:
        infoLabel.configure(text="")

def stopMusic():
    global song_selected
    pygame.mixer.init()
    pygame.mixer.music.load('shared_files/'+song_selected)
    pygame.mixer.music.pause()
    infoLabel.configure(text="")

def resume():
    global song_selected
    pygame.mixer.init()
    pygame.mixer.music.load('shared_files/'+song_selected)
    pygame.mixer.music.play()

def pause():
    global song_selected
    pygame.mixer.init()
    pygame.mixer.music.load('shared_files/'+song_selected)
    pygame.mixer.pause()

def musicWindow():
    global listBox
    global infoLabel
    global song_counter
    global filePathLabel

    window = Tk()
    window.title('Share Music')
    window.geometry('300x340')
    window.configure(bg='#93a9cc')

    selectSong = Label(window, text='Select Song', bg='#93a9cc', font=('Ink Free', 10))
    selectSong.place(x=10, y=1)

    # checking if 'shared_files' directory exists, and create it if not
    shared_files_path = 'shared_files'
    if not os.path.exists(shared_files_path):
        os.makedirs(shared_files_path)

    listBox= Listbox(window, height=8, width=39, activestyle='dotbox', font=('Ink Free', 10))
    listBox.place(x=10, y=25)

    for file in os.listdir('shared_files'):
        filename = os.fsdecode(file)
        listBox.insert(song_counter, filename)
        song_counter += 1

    scrollbar = Scrollbar(listBox)
    scrollbar.place(relheight=1, relx=1)
    scrollbar.config(command=listBox.yview)

    playButton = Button(window, text='Play', width=10, bd=1, bg='#eadeff', font=('Ink Free', 10), command=play)
    playButton.place(x=30, y=180)

    stop = Button(window, text='Stop', bd=1, width=10, bg='#eadeff', font=('Ink Free', 10), command=stopMusic)
    stop.place(x=200, y=180)

    resumeButton = Button(window, text="Resume", width=10, bd=1, bg='#eadeff', font=('Ink Free', 10), command=resume)
    resumeButton.place(x=30, y=220)

    pauseButton = Button(window, text="Pause", width=10, bd=1, bg='#eadeff', font=('Ink Free', 10), command=pause)
    pauseButton.place(x=200, y=220)

    upload = Button(window, text='Upload', bd=1, width=10, bg='#eadeff', font=('Ink Free', 10), command=browseFiles)
    upload.place(x=30, y=260)

    download = Button(window, text='Download', bd=1, width=10, bg='#eadeff', font=('Ink Free', 10), command=downloadFile)
    download.place(x=200, y=260)

    infoLabel = Label(window, text='', fg='blue', font=('Ink Free', 10))
    infoLabel.place(x=30, y=300)

    #available_fonts = font.families()
    #print(available_fonts)

    window.mainloop()

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS, PORT))
    musicWindow()

setup()