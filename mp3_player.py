from tkinter import *

#import pygame.mixer.music
from PIL import ImageTk, Image
from tkinter import filedialog, ttk
from pygame import mixer
import time
from mutagen.mp3 import MP3

mixer.init()
root = Tk()
root.title('MP3 Player')
root.geometry("420x290")

playlist = []

listbox = Listbox(root)
listbox.grid(row=0, column=0, sticky="NE")

def song_rename(songname):
    s = []
    lastindex = songname.rindex("/")
    for i in songname[lastindex+1:]:
        s.append(i)
    songname = ''.join(s)
    return songname

def convert_time(time):
    total_seconds = int(time)
    minutes = int(total_seconds/60)
    seconds = int(total_seconds - (minutes * 60))
    if seconds < 10:
        return str(minutes) + ":0" + str(seconds)
    else:
        return str(minutes) + ":" + str(seconds)

def add_song():
    mixer.music.pause()
    filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")))
    if filename != '':
        songname = song_rename(filename)
        songinfo = (songname, filename)
        playlist.append(songinfo)
        lastindex = len(playlist)-1
        listbox.insert(END, playlist[lastindex][0])
    mixer.music.unpause()

def remove_song():
    current = listbox.curselection()
    current = current[0]
    if current_song == playlist[current][1]:
        stop()
    listbox.delete(current)
    playlist.remove((playlist[current][0], playlist[current][1]))

def get_time():
    total_seconds = int(mixer.music.get_pos()/1000)
    song_mut = MP3(current_song)
    song_length = int(song_mut.info.length)
    if paused:
        pass
    else:
        if song_length == int(song_slider.get()):
            song_slider.config(to=song_length, value=song_length)
            elapsed_time.config(text=convert_time(song_length))
        #elif song_slider.get() != total_seconds:
            #song_slider.config(to=song_length, value=total_seconds)
            #elapsed_time.config(text=convert_time(total_seconds))
            #return
        else:
            song_slider.config(to=song_length,value=int(song_slider.get()))
            elapsed_time.config(text=convert_time(song_slider.get()))
            next_time = int(song_slider.get()) + 1
            song_slider.config(to=song_length, value=next_time)
    elapsed_time.after(1000, get_time)
    total_time.config(text=convert_time(song_length))

def stop():
    mixer.music.stop()
    song_slider.config(value=0)
    elapsed_time.config(text="0:00")

current_song = ''

def play():
    global current_song
    song_slider.config(value=0)
    elapsed_time.config(text="0:00")
    current = listbox.curselection()
    current = current[0]
    current_song = playlist[current][1]

    mixer.music.load(current_song)
    mixer.music.play()

    label.configure(text="Now Playing\n" + listbox.get(listbox.curselection()))

    get_time()

paused = False

def pause():
    global paused
    if (paused):
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True

def back():
    song_slider.config(value=0)
    elapsed_time.config(text="0:00")
    index = listbox.curselection() #changed
    index = index[0]
    if index == 0:
        listbox.selection_clear(0, END)
        listbox.selection_set(listbox.size()-1)
        mixer.music.load(playlist[listbox.size()-1][1])
        mixer.music.play()
        label.configure(text="Now Playing\n" + listbox.get(listbox.size()-1))
    else:
        prev_song = listbox.curselection() #changed
        prev_song = prev_song[0] - 1
        mixer.music.load(playlist[prev_song][1])
        mixer.music.play()
        listbox.selection_clear(0,END)
        listbox.selection_set(prev_song)
        label.configure(text="Now Playing\n" + listbox.get(listbox.curselection()))

def next():
    song_slider.config(value=0)
    elapsed_time.config(text="0:00")
    index = listbox.curselection() #changed
    index = index[0]
    if index == listbox.size() - 1:
        listbox.selection_clear(0, END)
        listbox.selection_set(0)
        mixer.music.load(playlist[0][1])
        mixer.music.play()
        label.configure(text="Now Playing\n" + listbox.get(0))
    else:
        next_song= listbox.curselection() #changed
        next_song = next_song[0] + 1
        mixer.music.load(playlist[next_song][1])
        mixer.music.play()
        listbox.selection_clear(0, END)
        listbox.selection_set(next_song)
        label.configure(text="Now Playing\n" + listbox.get(listbox.curselection()))

def scrub(time):
    current = listbox.curselection()
    current = current[0]

    mixer.music.load(playlist[current][1])
    mixer.music.play(start=song_slider.get())

def volume(vol):
    mixer.music.set_volume(volume_slider.get())

#images
img1 = PhotoImage(file='images/back.png')
img2 = PhotoImage(file='images/next.png')
img3 = PhotoImage(file='images/pause.png')
img4 = PhotoImage(file='images/play.png')
img5 = PhotoImage(file='images/volume.png')

btn = Button(root, text="Add Song", command=add_song).grid(row=1,column=0)
remove_btn = Button(root, text="Remove Song", command=remove_song).grid(row=2, column=0)
back_btn = Button(root, image=img1, command=back).grid(row=1,column=2, sticky=E)
play_btn = Button(root, image=img4, command=play).grid(row=1,column=3, sticky=E)
pause_btn = Button(root, image=img3, command=pause).grid(row=1,column=4, sticky=E)
next_btn = Button(root, image=img2, command=next).grid(row=1,column=5, sticky=E)

blanklabel = Label(root).grid(row=1,column=1)

volume_frame = LabelFrame(root, bd=0)
volume_frame.grid(row=0, column=6, columnspan=5)

label = Label(root, text="Now Playing",font=("Courier", 15), wraplength=180)
label.grid(row=0,column=2, columnspan=5)

elapsed_time = Label(root, text="")
elapsed_time.grid(row=3,column=2)

total_time = Label(root, text="")
total_time.grid(row=3,column=5)

song_slider = ttk.Scale(root, from_=0, to=1, orient=HORIZONTAL, value=0, command=scrub, length=200)
song_slider.grid(row=2, column=2, columnspan=5)

volume_label = Label(volume_frame, image=img5).pack()
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=160)
volume_slider.pack()

root.mainloop()