from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("Music player")
root.geometry("500x400")

#initializing pygame
pygame.mixer.init()

#create function to play with time
def play_time():

    #check if song is stopped or not
    if stopped:
        return
    #grab current song time
    current_time = pygame.mixer.music.get_pos()/1000
    #setting time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = playlist_box.get(ACTIVE)
    # reconstruct song with directory
    song = f'E:/pycharm/Prit/Project/MP3/audio/{song}.mp3'

    #find current song length
    song_mut = MP3(song)
    global song_len
    song_len = song_mut.info.length
    #convert to time format
    converted_song_len = time.strftime('%M:%S', time.gmtime(song_len))

    #check to see if song is over
    if int(song_len) == int(song_slider.get()):
        return stop()

    elif paused:
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
        # output slider
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_len}   ')
    else:
        #move slider along one second at a time
        next_time = int(song_slider.get()) + 1
        #output new time value to slider
        song_slider.config(to = song_len,value = next_time)
        #convert slider position to time format
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
        #output slider
        status_bar.config(text = f'Time Elapsed: {converted_current_time} of {converted_song_len}   ')

    if current_time>=1:
        #add current time to status bar
        status_bar.config(text = f'Time Elapsed: {converted_current_time} of {converted_song_len}   ')
    #check current time after 1 sec
    status_bar.after(1000,play_time)

# create function to add one song
def add_song():
    song = filedialog.askopenfilename(initialdir = 'audio/', title = "choose a song", filetypes = (("mp3 Files","*.mp3"),))
    #Strip path to get just name of song
    song = song.replace("E:/pycharm/Prit/Project/MP3/audio/","")
    song = song.replace(".mp3","")
    playlist_box.insert(END, song)

#create function to add many songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="choose songs", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        # Strip path to get just name of song
        song = song.replace("E:/pycharm/Prit/Project/MP3/audio/", "")
        song = song.replace(".mp3", "")
        playlist_box.insert(END, song)

#create function to delete one song
def delete_song():
    #delete highlighted song
    playlist_box.delete(ANCHOR)

#create function to delete all song
def delete_all_songs():
    playlist_box.delete(0,END)

#create play button
def play():
    #when we play song agian or different song set stopped to False
    global stopped
    stopped = False
    song = playlist_box.get(ACTIVE)
    #reconstruct song with directory
    song = f'E:/pycharm/Prit/Project/MP3/audio/{song}.mp3'
    # load song with pygame
    pygame.mixer.music.load(song)
    #play song with pygame
    pygame.mixer.music.play(loops=0)
    #get song time
    play_time()

#create stopped variable
global stopped
stopped = False

#create stop button
def stop():
    #stop song
    pygame.mixer.music.stop()
    #clear that selection of song from playlist
    playlist_box.select_clear(ACTIVE)
    status_bar.config(text = '')
    song_slider.config(value = 0)
    #set stopped variable to true
    global stopped
    stopped = True


#create paused variable
global paused
paused = False

#create pause button
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #pose
        pygame.mixer.music.pause()
        paused = True

#create forward song function
def next_song():
    #Reset slider position and status bar
    status_bar.config(text = 0)
    song_slider.config(value = 0)
    #get current song number
    next_one = playlist_box.curselection()
    #add 1 to current song(next song)
    next_one = next_one[0] + 1
    #grab the song title
    song = playlist_box.get(next_one)
    # reconstruct song with directory
    song = f'E:/pycharm/Prit/Project/MP3/audio/{song}.mp3'
    # load song with pygame
    pygame.mixer.music.load(song)
    # play song with pygame
    pygame.mixer.music.play(loops=0)
    #clear active selection
    playlist_box.selection_clear(0,END)
    #move active bar to next song
    playlist_box.activate(next_one)
    #set active bar to next song
    playlist_box.selection_set(next_one,last=None)

#create back button
def previous_song():
    # Reset slider position and status bar
    status_bar.config(text=0)
    song_slider.config(value=0)
    # get current song number
    previous_one = playlist_box.curselection()
    # add 1 to current song(next song)
    previous_one = previous_one[0] - 1
    # grab the song title
    song = playlist_box.get(previous_one)
    # reconstruct song with directory
    song = f'E:/pycharm/Prit/Project/MP3/audio/{song}.mp3'
    # load song with pygame
    pygame.mixer.music.load(song)
    # play song with pygame
    pygame.mixer.music.play(loops=0)
    # clear active selection
    playlist_box.selection_clear(0, END)
    # move active bar to next song
    playlist_box.activate(previous_one)
    # set active bar to next song
    playlist_box.selection_set(previous_one, last=None)

#create volumn function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

#create song slider
def slide(x):
    song = playlist_box.get(ACTIVE)
    # reconstruct song with directory
    song = f'E:/pycharm/Prit/Project/MP3/audio/{song}.mp3'
    # load song with pygame
    pygame.mixer.music.load(song)
    # play song with pygame
    pygame.mixer.music.play(loops=0, start=song_slider.get())


#create main_frame
main_frame = Frame(root)
main_frame.pack(pady=20)

# create playlist box
playlist_box = Listbox(main_frame, bg = "black", fg = "green", width =60,selectbackground = "green", selectforeground = "black")
playlist_box.grid(row=0,column=0)

#create volume slider frame
volume_frame = LabelFrame(main_frame, text = "Volume")
volume_frame.grid(row=0,column=1,padx=20)

#create slider for volumne
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient = VERTICAL, length = 125,value=1, command = volume)
volume_slider.pack(pady=10)

#create song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient = HORIZONTAL, length = 350,value=0, command = slide)
song_slider.grid(row=2,column=0, pady=20)

# define button images for controls
back_btn_img = PhotoImage(file = 'images/back50.png')
forward_btn_img = PhotoImage(file = 'images/forward50.png')
play_btn_img = PhotoImage(file = 'images/play50.png')
pause_btn_img = PhotoImage(file = 'images/pause50.png')
stop_btn_img = PhotoImage(file = 'images/stop50.png')

# create button frame
control_frame = Frame(main_frame)
control_frame.grid(row=1,column=0,pady = 20)

# create play/pause etc buttons
back_button = Button(control_frame, image = back_btn_img, borderwidth = 0, command = previous_song)
forward_button = Button(control_frame, image = forward_btn_img, borderwidth = 0, command = next_song)
play_button = Button(control_frame, image = play_btn_img, borderwidth = 0, command = play)
pause_button = Button(control_frame, image = pause_btn_img, borderwidth = 0, command = lambda: pause(paused))
stop_button = Button(control_frame, image = stop_btn_img, borderwidth = 0, command = stop)

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

# creating a menu
my_menu = Menu(root)
root.config(menu = my_menu)

# create add song meu dropdowns
add_song_menu = Menu(my_menu, tearoff = 0)
my_menu.add_cascade(label = "Add Songs", menu = add_song_menu)
#add one song to playlist
add_song_menu.add_command(label = "Add one song to playlist", command = add_song)
#add more sond to playlist
add_song_menu.add_command(label = "Add many songs to playlist", command = add_many_songs)

# create add song meu dropdowns
remove_song_menu = Menu(my_menu, tearoff = 0)
my_menu.add_cascade(label = "Delete songs", menu = remove_song_menu)
remove_song_menu.add_command(label = "Remove one song to playlist", command = delete_song)
remove_song_menu.add_command(label = "Remove all songs to playlist", command = delete_all_songs)

#create status bar
status_bar = Label(root, text = '', bd=1, relief = GROOVE, anchor = E)
status_bar.pack(fill = X, side = BOTTOM, ipady = 2)

#temporary label
l = Label(root,text='')
l.pack(pady=20)
root.mainloop()