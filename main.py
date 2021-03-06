from pygame import mixer  
import tkinter as tk
import requests
import psycopg2
import os.path
import smtplib
import time
import os

# variables for main window size (pixels)

HEIGHT = 800
WIDTH = 1200

# image paths

MAIN_ICON = os.path.join('/','home', 'vladimir','Documents','programming','mp3player','pictures', 'main_icon3.png')

# colors 

SAILOR_BLUE = '#296C92'
MINT_GREEN = '#CFFFE5'
WHITE = '#FFFFFF'
WARNING_RED = '#E60000'

# main window options

root = tk.Tk()
root.title('MP3 player by vladimirferko')
root.geometry('{}x{}'.format(WIDTH, HEIGHT))
root.resizable(0,0)

img = tk.PhotoImage(file= MAIN_ICON)
root.tk.call('wm', 'iconphoto', root._w, img)

# connection with postgres database using psycopg2 module

conn = psycopg2.connect(
    host = 'localhost',
    database = 'mp3playerApp',
    user = 'postgres',
    password = 'password'
)
conn.set_session(autocommit = True)


# login / register / using interface class

class LoginWindow:
    login_x_value = (WIDTH / 3) / 10
    entry_width = 25
    cursor = conn.cursor()
    EMAIL_ADRESS = 'YOUR EMAIL'
    EMAIL_PASSWORD = 'PASSWORD FOR YOUR EMAIL'
    MUSIC_DIR = os.path.join('/','home', 'vladimir','Documents','programming','mp3player','storage')

    def __init__(self, master):
        self.main_frame = tk.Frame(master, width = WIDTH, height = HEIGHT, bg = SAILOR_BLUE)
        self.main_frame.pack()

        self.intro_label = tk.Label(self.main_frame, text = 'Welcome to the MP3 player by vladimirferko', bg = SAILOR_BLUE, fg = MINT_GREEN, font = ('Calibri', 18))
        self.intro_label.place(x = WIDTH / 3.5, y = HEIGHT / 10)

        # bottom frame and its labels, there are clock and contact of this app

        self.bottom_frame = tk.Frame(self.main_frame, width = WIDTH, height = HEIGHT / 10, bg = MINT_GREEN)
        self.bottom_frame.place(x = 0, y = HEIGHT - (HEIGHT / 10))

        self.clock = tk.Label(self.bottom_frame, font = ('Calibri', 15),bg = SAILOR_BLUE, fg = MINT_GREEN)
        self.clock.place(x = WIDTH - (WIDTH / 5), y = (HEIGHT / 10) / 3)
        self.get_time()

        self.contact_label = tk.Label(self.bottom_frame, bg = SAILOR_BLUE, fg = MINT_GREEN ,text = '  Contact me at YOUR EMAIL  \n  or at YOUR PHONEq  ')
        self.contact_label.place(x = 15, y = (HEIGHT / 10) / 3)

        # login frame and its entry boxes and so on...

        self.login_frame = tk.Frame(self.main_frame, width = WIDTH / 3, height = HEIGHT / 3, bg = MINT_GREEN)
        self.username_label = tk.Label(self.login_frame, text = 'username : ', bg = MINT_GREEN, fg = SAILOR_BLUE, font = ('Calibri', 10))
        self.username_entry = tk.Entry(self.login_frame, width = LoginWindow.entry_width, bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat')
        self.password_label = tk.Label(self.login_frame, text = 'password : ', bg = MINT_GREEN, fg = SAILOR_BLUE, font = ('Calibri', 10))
        self.password_entry = tk.Entry(self.login_frame, show = '*' ,width = LoginWindow.entry_width, bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat')
        self.login_button = tk.Button(self.login_frame, text = 'Login', bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat', command = self.login_func)
        self.register_button = tk.Button(self.login_frame, text = "I don't have an accout yet",  bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat', command = self.register_func)
        self.wrong_login = tk.Label(self.login_frame, text = 'User not found',bg = WARNING_RED, fg = WHITE)

        self.login_frame.place(x = WIDTH / 2 - (WIDTH / 3) / 2, y = (HEIGHT - (HEIGHT / 1.5)) / 2)

        self.login_widget_tuple = (self.username_label, self.username_entry, self.password_label, self.password_entry, self.register_button, self.login_button)
        self.login_entry_tuple = (self.username_entry, self.password_entry)




        for index, item in enumerate(self.login_widget_tuple):
            if index < 4:
                item.place(x = LoginWindow.login_x_value , y = ((HEIGHT / 2.5) / 10) + index * 25)
            else:
                item.place(x = LoginWindow.login_x_value , y = ((HEIGHT / 2.5) / 10) + index * 30)

        # widgets for registrating users

        self.register_frame = tk.Frame(self.main_frame, width = WIDTH / 3, height = HEIGHT / 2, bg = MINT_GREEN)

        self.register_email_label = tk.Label(self.register_frame, text = 'email :', bg = MINT_GREEN, fg = SAILOR_BLUE, font = ('Calibri', 10))
        self.register_email_entry = tk.Entry(self.register_frame, width = LoginWindow.entry_width, bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat')

        self.register_name_label = tk.Label(self.register_frame, text = 'username : ', bg = MINT_GREEN, fg = SAILOR_BLUE, font = ('Calibri', 10))
        self.register_name_entry = tk.Entry(self.register_frame, width = LoginWindow.entry_width, bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat')

        self.register_password1_label = tk.Label(self.register_frame, text = 'password : ', bg = MINT_GREEN, fg = SAILOR_BLUE, font = ('Calibri', 10))
        self.register_password1_entry = tk.Entry(self.register_frame, width = LoginWindow.entry_width, bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat', show = '*')

        self.register_password2_label = tk.Label(self.register_frame, text = 'repeat your password :', bg = MINT_GREEN, fg = SAILOR_BLUE, font = ('Calibri', 10))
        self.register_password2_entry = tk.Entry(self.register_frame, width = LoginWindow.entry_width, bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat', show = '*')

        self.register_exit_button = tk.Button(self.register_frame, text = 'exit', bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat', command = self.exit_registration_func)
        self.register_confirm_button = tk.Button(self.register_frame, text = 'Confirm registration', bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat', command = self.confirm_registration_func)

        self.register_widget_tuple = (self.register_email_label, self.register_email_entry, self.register_name_label, self.register_name_entry, self.register_password1_label, self.register_password1_entry, self.register_password2_label, self.register_password2_entry, self.register_confirm_button, self.register_exit_button)
        self.register_entry_tuple = (self.register_email_entry, self.register_name_entry, self.register_password1_entry, self.register_password2_entry)

        # these widgets will appear if something will go wrong

        self.error_widget = tk.Label(self.register_frame, bg = WARNING_RED, fg = WHITE)




        # main window widgets and functions from here --------

        self.white_stick = tk.Canvas(self.main_frame, width = 3, height = HEIGHT / 1.5, bg = WHITE)
        
        self.logged_user_button = tk.Button(self.main_frame, bg = MINT_GREEN, fg = SAILOR_BLUE, font = ('Calibri', 12), padx = 5, pady = 5, command = self.enter_log_nick, relief = 'flat')

        self.logged_user_opts = tk.Frame(self.main_frame, bg = MINT_GREEN, width = WIDTH / 4, height = HEIGHT / 4)
        self.logged_user_opts.bind("<Leave>", self.leave_log_nick)    

        self.logged_user_label = tk.Label(self.logged_user_opts, bg = MINT_GREEN, fg = SAILOR_BLUE, font = ('Calibri', 12))
        self.logout_button = tk.Button(self.logged_user_opts, text = 'Logout', bg = SAILOR_BLUE, fg = MINT_GREEN, relief = 'flat', pady = 10, padx = 10, command = self.logout_func)
        self.login_time_label = tk.Label(self.logged_user_opts, bg = SAILOR_BLUE, fg = MINT_GREEN)

        self.song_frame = tk.Frame(self.main_frame, width = WIDTH / 4, height = HEIGHT / 2, bg = MINT_GREEN)

        self.scrollbar = tk.Scrollbar(self.song_frame)

        self.play_menu = tk.Frame(self.main_frame, width = WIDTH / 2, height = HEIGHT / 8, bg = MINT_GREEN)


        self.play_stop_button = tk.Button(self.play_menu, text = 'STOP', bg = SAILOR_BLUE, font = ('Calibri', 12), fg = WHITE, command = self.play_stop_func)
        self.play_next_button = tk.Button(self.play_menu, text = 'Next song', bg = SAILOR_BLUE, font = ('Calibri', 12), fg = WHITE, command = self.next_song_func)
        self.play_previous_button = tk.Button(self.play_menu, text = 'Previous song', bg = SAILOR_BLUE, font = ('Calibri', 12), fg = WHITE, command = self.prev_song_func)

        self.song_img = tk.PhotoImage(file = 'pictures/tune (2).png')
        self.song_img_label = tk.Label(self.main_frame, image = self.song_img)

        self.song_lbl = tk.Label(self.main_frame, fg = WHITE, bg = SAILOR_BLUE, font = ('Calibri', 12))


    # function which gives me a time

    def get_time(self):
        self.timeVar = time.strftime('%H:%M:%S')
        self.clock.config(text = '  ' + self.timeVar + '                    ')
        self.clock.after(500, self.get_time)

    # function for registrating new users

    def register_func(self):
        self.login_frame.place_forget()
        self.register_frame.place(x = WIDTH / 2 - (WIDTH / 3) / 2, y = (HEIGHT - (HEIGHT / 1.5)) / 2)


        self.show_register_widgets()

    # exit registration function

    def exit_registration_func(self):
        self.register_frame.place_forget()
        self.login_frame.place(x = WIDTH / 2 - (WIDTH / 3) / 2, y = (HEIGHT - (HEIGHT / 1.5)) / 2)
        
        self.show_login_widgets()

    # 2 functions for showing widgets on the screen 

    def show_login_widgets(self):
        for index, item in enumerate(self.login_widget_tuple):
            if index < 4:
                item.place(x = LoginWindow.login_x_value , y = ((HEIGHT / 2.5) / 10) + index * 25)
            else:
                item.place(x = LoginWindow.login_x_value , y = ((HEIGHT / 2.5) / 10) + index * 30)
        
        
        for item in self.register_entry_tuple:
            item.delete(0, 'end')


    def show_register_widgets(self):
        for index, item in enumerate(self.register_widget_tuple):
            if index < 8:
                item.place(x = LoginWindow.login_x_value , y = ((HEIGHT / 2.5) / 10) + index * 25)
            else: 
                item.place(x = LoginWindow.login_x_value , y = ((HEIGHT / 6) / 10) + (index * 28) + 20)

        for item in self.login_entry_tuple:
            item.delete(0, 'end')


    # function for confirming registrations, writing to database and so on

    def confirm_registration_func(self):
        self.email_address = self.register_email_entry.get().strip()
        self.response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params = {'email': self.email_address})

        LoginWindow.cursor.execute(
            "SELECT * FROM users"
        )
        self.user_database = LoginWindow.cursor.fetchall()

        # if app has no users it will check for requirements in this if statement and here 

        if len(self.user_database) == 0:


            if self.response.json()['status'] != 'valid':
                self.error_widget.configure(text = "This email adress doesn't exist")
                self.error_widget.place(x = LoginWindow.login_x_value, y = HEIGHT / 2.5)
            elif len(self.register_password1_entry.get()) < 6:
                self.error_widget.configure(text = 'Password has to be at least 6 characters long')
                self.error_widget.place(x = LoginWindow.login_x_value, y = HEIGHT / 2.5)

            elif self.register_entry_tuple[2].get() != self.register_entry_tuple[3].get():
                self.error_widget.configure(text = "Passwords doesn't match")
                self.error_widget.place(x = LoginWindow.login_x_value, y = HEIGHT / 2.5)
            else:
                self.error_widget.place_forget()
                LoginWindow.cursor.execute(
                    f"INSERT INTO users (user_email, user_name, user_password) VALUES ('{self.register_entry_tuple[0].get()}', '{self.register_entry_tuple[1].get()}', '{self.register_entry_tuple[2].get()}')"
                )
                
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login(LoginWindow.EMAIL_ADRESS, LoginWindow.EMAIL_PASSWORD)
                    smtp.sendmail(LoginWindow.EMAIL_ADRESS, f'{self.register_email_entry.get()}', f'Hi {self.register_name_entry.get()} \nthank you for your registration')

                for item in self.register_entry_tuple:
                        item.delete(0, 'end')

        # here program will loop through users in database and check if there is user with certain email or username and so on

        else:

            for item in self.user_database:
                if self.response.json()['status'] != 'valid':
                    self.error_widget.configure(text = "This email adress doesn't exist")
                    self.error_widget.place(x = LoginWindow.login_x_value, y = HEIGHT / 2.5)

                elif item[1] == self.register_entry_tuple[0].get():
                    self.error_widget.config(text = 'This email adress is already used')
                    self.error_widget.place(x = LoginWindow.login_x_value, y = HEIGHT / 2.5)

                elif item[2] == self.register_entry_tuple[1].get():
                    self.error_widget.configure(text = 'This username is already used')
                    self.error_widget.place(x = LoginWindow.login_x_value, y = HEIGHT / 2.5)

                elif len(self.register_password1_entry.get()) < 6:
                    self.error_widget.configure(text = 'Password has to be at least 6 characters long')
                    self.error_widget.place(x = LoginWindow.login_x_value, y = HEIGHT / 2.5)

                elif self.register_entry_tuple[2].get() != self.register_entry_tuple[3].get():
                    self.error_widget.configure(text = "Passwords doesn't match")
                    self.error_widget.place(x = LoginWindow.login_x_value, y = HEIGHT / 2.5)

                else:
                    self.error_widget.place_forget()
                    LoginWindow.cursor.execute(
                        f"INSERT INTO users (user_email, user_name, user_password) VALUES ('{self.register_entry_tuple[0].get()}', '{self.register_entry_tuple[1].get()}', '{self.register_entry_tuple[2].get()}')"
                    )

                    

                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(LoginWindow.EMAIL_ADRESS, LoginWindow.EMAIL_PASSWORD)
                        smtp.sendmail(LoginWindow.EMAIL_ADRESS, f'{self.register_email_entry.get()}', f'Hi {self.register_name_entry.get()} \nthank you for your registration')

                    for item in self.register_entry_tuple:
                        item.delete(0, 'end')


    # function for logging in, just for registrated users

    def login_func(self):

        # calling SELECT * again, because an user can be registered so i need to overwrite my variable with new users

        LoginWindow.cursor.execute(
            "SELECT * FROM users"
        )

        self.user_database = LoginWindow.cursor.fetchall()


        for item in self.user_database:
            if self.username_entry.get().strip() == item[2].strip() and self.password_entry.get().strip() == item[3].strip():
                self.wrong_login.place_forget()
                self.login_frame.place_forget()
                self.intro_label.place_forget()

                self.show_default_app()

                self.logged_user_button.configure(text = item[2].strip())

                self.login_time = time.strftime('%H:%M')
                self.login_time_label.config(text = f'Online since {self.login_time}')
                self.login_time_label.place(relx = 0.5, rely = 0.8)
                
            else:
                self.wrong_login.place(x = LoginWindow.login_x_value , y = ((HEIGHT / 2.5) / 10) + 185)
                

    # this func makes us show widgets after logging in

    def show_default_app(self):
        self.white_stick.place(x = WIDTH / 3.5, y = HEIGHT / 8)
        self.logged_user_button.place(x = 0, y = 0)
        self.song_frame.place(x = 20, y = 225)

        self.song_arr = []
        self.song_arr_names = []

        index = 0
        for song in os.listdir(LoginWindow.MUSIC_DIR):
            if song.endswith('.ogg') or song.endswith('.mov'):
                self.song_arr.append(tk.Button(self.song_frame, text = f'{str(index)} - {song[0:32]}', relief = 'flat', bg = MINT_GREEN, fg = SAILOR_BLUE, command = lambda song = song: self.play_song(song)))
                self.song_arr[index].place(x = 15, y = 15 + (index * 50))
                self.song_arr_names.append(song)
                index += 1

    # functions for having cursor on logged nick

    def enter_log_nick(self):
        self.logged_user_opts.place(x = 20, y = 20)
        self.logged_user_label.configure(text = self.logged_user_button.cget('text'))
        self.logged_user_label.place(relx = 0.3, rely = 0.2)
        self.logout_button.place(relx = 0.3, rely = 0.5)

    # function to play music

    def play_song(self, song):
        os.chdir(LoginWindow.MUSIC_DIR)
        mixer.init()
        mixer.music.stop()
        mixer.music.load(song)
        mixer.music.play()
        self.song_lbl.configure(text = song[:len(song) - 4])
        self.song_lbl.place(x = 575, y = 110)
        self.play_menu.place(x = 475, y = 600)
        self.play_stop_button.place(x = 270, y = 30)
        self.play_next_button.place(x = 450, y = 30)
        self.play_previous_button.place(x = 50 , y = 30)

        self.song_img_label.place(x = 575, y = 150)


    def leave_log_nick(self, event):
        self.logged_user_opts.place_forget()

    # leaving all logged in widgets 

    def leave_main_app(self):
        self.logged_user_button.place_forget()
        self.white_stick.place_forget()
        self.logged_user_opts.place_forget()
        self.song_frame.place_forget()
        self.song_img_label.place_forget()
        self.play_menu.place_forget()
        self.song_lbl.place_forget()
        self.wrong_login.place_forget()
        mixer.music.unload()
        mixer.music.stop()

    # logout function

    def logout_func(self):
        self.login_frame.place(x = WIDTH / 2 - (WIDTH / 3) / 2, y = (HEIGHT - (HEIGHT / 1.5)) / 2)
        self.leave_main_app()
        self.show_register_widgets()


    # function for playing and stopping the song 

    def play_stop_func(self):
        if self.play_stop_button.cget('text') == 'STOP':
            self.play_stop_button.configure(text = 'PLAY')
            mixer.music.pause()
        else:
            self.play_stop_button.configure(text = 'STOP')
            mixer.music.unpause()

    # function for playing next song 

    def next_song_func(self):

        for index ,item in enumerate(self.song_arr_names):
            if self.song_lbl.cget('text') == item[:-4]:
                if self.song_arr_names.index(item) >= len(self.song_arr_names) - 1:
                    print('Too much')
                    break
                else:
                    self.play_song(self.song_arr_names[index + 1])
                    break


    # function for playing previous song

    def prev_song_func(self):

        for index ,item in enumerate(self.song_arr_names):
            if self.song_lbl.cget('text') == item[:-4]:
                if self.song_arr_names.index(item) <= 0:
                    mixer.music.rewind()
                    break
                else:
                    self.play_song(self.song_arr_names[index - 1])
                    break



login = LoginWindow(root)


root.mainloop()