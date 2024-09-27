import customtkinter as ck
from PIL import Image
from threading import Thread
from bartimaeus_sr import start_program
from bartimaeus_db import Database

# ---------------------------db initialisation----------------------------------------------
db = Database()
db.connect()

# db.create_table("bartimaeusContactList", "id INTEGER PRIMARY KEY autoincrement, name varchar(25), email varchar(45)")
# db.create_table("bartimaeusEmailHistory", "id INTEGER PRIMARY KEY autoincrement, email varchar(45), name varchar(25), email_subject varchar(100), email_message varchar(200), send_status varchar(10), send_time datetime default current_timestamp")


# db.insert_data("bartimaeusContactList", "'Tayo', 'tayo@gmail.com'")
# db.insert_data("bartimaeusContactList", "'Nana', 'omma@gmail.com'")
# db.insert_data("bartimaeusContactList", "'Uyoz', 'uyoz@gmail.com'")
# db.insert_data("bartimaeusContactList", "'Taga', 'outofoffice@gmail.com'")
# db.insert_data("bartimaeusContactList", "'John', 'ade@gmail.com'")
# db.insert_data("bartimaeusContactList", "'Ifa', 'fk@gmail.com'")
# db.insert_data("bartimaeusEmailHistory", "'fk@gmail.com','John','Vacation plans','When are you going on vacation?','sent'")



class Window():
    def __init__(self):
        
        #GUI Window
        self.window  = ck.CTk(fg_color='#fff')
        self.window.title('Email Sender')
        self.window.geometry('850x750')
        self.window.grid_columnconfigure(1,weight=1)

        
        #side frame
        self.side_frame = ck.CTkFrame(self.window,fg_color='#00425f', corner_radius=0)
        self.side_frame.grid(column=0,sticky = 'ns', rowspan =7,pady=(10,0),ipadx =25)
        self.side_frame.grid_columnconfigure(0,weight=1)
        self.side_frame.grid_rowconfigure(7,weight=1)

        #content frame
        self.content_frame = ck.CTkFrame(self.window,fg_color='#e9f5f9')
        self.content_frame.grid(row=0,column=1, padx=10,pady=(10,0),sticky='ewns')
        self.content_frame.grid_columnconfigure((1),weight=1)


        #***********************************side frame content***********************************

        #side frame logo
        self.isw_logo = ck.CTkImage(light_image=Image.open("gmail-logo.png"),size=(144, 100))
        self.side_logo = ck.CTkLabel(self.side_frame, image=self.isw_logo, text="")
        self.side_logo.grid(row=0,column=0, pady=20,padx=10)

        #side frame Inbox button
        self.compose_button = ck.CTkButton(self.side_frame, text = 'Compose',text_color='#fff',command = lambda:self.thread_run(self))
        self.compose_button.grid(row = 1, column = 0, padx =20, pady =10)

        #side frame Inbox button
        self.inbox_button = ck.CTkButton(self.side_frame, text = 'Inbox',text_color='#fff',command = self.buttons_callback)
        self.inbox_button.grid(row = 2, column = 0, padx =20, pady =10)

        #side frame Sent button
        self.sent_button = ck.CTkButton(self.side_frame, text = 'Sent',text_color='#fff',command = self.buttons_callback)
        self.sent_button.grid(row = 3, column = 0, padx =20, pady =10)

        #side frame Draft button
        self.draft_button = ck.CTkButton(self.side_frame, text = 'Draft',text_color='#fff',command = self.buttons_callback)
        self.draft_button.grid(row = 4, column = 0, padx =20, pady =10)

        #side frame Spam button
        self.spam_button = ck.CTkButton(self.side_frame, text = 'Spam',text_color='#fff',command = self.buttons_callback)
        self.spam_button.grid(row = 5, column = 0, padx =20, pady =10)

        #side frame Trash button
        self.trash_button = ck.CTkButton(self.side_frame, text = 'Trash',text_color='#fff',command = self.buttons_callback)
        self.trash_button.grid(row = 6, column = 0, padx =20, pady =10)
        
        #side frame text
        self.side_label = ck.CTkLabel(self.side_frame, text="Bartimeus \n a voice-activated \n email sender",text_color='#fff',font=ck.CTkFont('stylus',30))
        self.side_label.grid(row =7, sticky='s',pady=10)


        #********************************content frame content**********************************

        
        #recipient name label
        self.name_label = ck.CTkLabel(self.content_frame, text = 'Recipient\'s Name:',text_color='#00425f')
        self.name_label.grid(row = 1, column = 0, padx =20, pady =10, sticky = 'w')

        #recipient name Entry
        self.name_entry = ck.CTkEntry(self.content_frame,border_color='#00425f',placeholder_text='Enter Recipient\'s Name',width=500,border_width = 1)
        self.name_entry.grid(row = 1, column = 1, padx =20, pady =10, sticky ='w')
        
        #-----------------------------------------------------------------

        #email address label
        self.email_label = ck.CTkLabel(self.content_frame, text = 'Recipient\'s Email Address:',text_color='#00425f')
        self.email_label.grid(row = 2, column = 0, padx =20, pady =10, sticky='w')

        #email address entry
        self.email_entry = ck.CTkEntry(self.content_frame,border_color='#00425f',placeholder_text='Enter Recipient\'s Email Address',width=500,border_width = 1)
        self.email_entry.grid(row = 2, column = 1, padx =20, pady =10, sticky='w')

        #-----------------------------------------------------------------

        #email subject label
        self.subject_label = ck.CTkLabel(self.content_frame, text = 'Email Subject:',text_color='#00425f')
        self.subject_label.grid(row = 3, column = 0, padx =20, pady =10, sticky='w')

        #email subject entry
        self.subject_entry = ck.CTkEntry(self.content_frame,border_color='#00425f',placeholder_text='Enter Email Subject',width=500,border_width = 1)
        self.subject_entry.grid(row = 3, column = 1, padx =20, pady =10,sticky='w')

        #-----------------------------------------------------------------

        #email body label
        self.message_label = ck.CTkLabel(self.content_frame, text = 'Email Body:',text_color='#00425f')
        self.message_label.grid(row = 4, column = 0, padx =20, pady =10, sticky='w')

        #email body entry
        self.message_entry = ck.CTkTextbox(self.content_frame,border_color='#00425f',width=500,border_width = 1)
        self.message_entry.grid(row = 4, column = 1, padx =20, pady = 10,sticky='w')


        #-----------------------------------------------------------------

        #console label 
        self.console_label = ck.CTkLabel(self.content_frame, text = '   Console   ',corner_radius= 2,fg_color='#00425f',text_color='#fff')
        self.console_label.grid(row = 5, column = 0, padx =20, pady =(10,0), sticky='w')

        #console entry
        self.console_entry = ck.CTkTextbox(self.content_frame,border_color='#00425f',width=708,border_width = 1)
        self.console_entry.grid(row = 6,column =0, pady=(0,5),padx = 10, sticky='wns',columnspan = 2)



        self.window.after(2000,self.thread_run,self)
        self.window.mainloop()
    
    #--------------------------------------------------------------------------

    def buttons_callback(self):
        self.console_entry.delete("0.0", "end")
        output='Don\'t bother clicking me. Uyi didn\'t configure me to do anything useful. I\'m nothing but a useless button. I feel so sad 😢 '
        self.console_entry.insert('0.0',output)   

    def thread_run(self, GUI):
        Thread(target=start_program, args = (GUI,)).start() 


#---------------------------------------------------------------------------------------------------

app = Window()
app
