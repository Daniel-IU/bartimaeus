# Bartimaeus
A simple voice-activated email sender developed using Python. The application's name is inspired by a blind Bible character named Bartimaeus. I have fixed all the bugs I encountered, so if you still encounter some bugs, please let me know.

# Package requirements
## Built-in packages (no need for pip install)
   
1. time
2. datetime
3. sys
4. re
5. threading
6. sqlite3
7. email (optional)
8. smtplib (optional)

## 3rd party packages (Run pip install)
1. pyttsx3
2. speech_recognition
3. customtkinter
4. Pillow
5. dateutil (run pip install python-dateutil or pip install pandas)
6. pyodbc
7. yagmail (optional) (might also need to run pip install keyring)

# Available files

1. **bartimaeus_gui_main.py:**
      This is the application's entry point, run this file to start the program. It contains the application's gui code and some db initialising code. You can optionally uncomment the db initalization section to create a sqlite3 db and the required tables with test data inserted. The gui code uses a third party library called customtkinter, it offers better-looking gui elements/widgets than the normal tkinter. Do not forget to run pip install customtkinter.

2. **bartimaeus_sr.py:**
       This is the speech recognition module, there's a whole lot going on here.

3. **bartimaeus_email.py:**
       This is the email sending module. Choose between two functions provided: Option 1 uses the built-in smtplib and email libraries, it works fine but the syntax seems quite verbose. Option 2 uses a third-party library called yagmail, it works fine as well but has a more concise syntax. If you choose this option (recommended) do not forget to run pip install yagmail (you might also need to run pip install keyring). For both options, connect/login using your email address and an app password (generated for you by google) not your regular account password. Please run a google search to see how to create an app password.

4. **bartimaeus_db.py:**
       This is the database module. Currently it works with the built-in sqlite3 package, if you want to connect to MS SQL Server, there are a number of things that should be changed in this file as both SQL dialects have different syntax. You can also work with the error messages you get to make the necessary modifications.

5. **gmail-logo.png:**
       This is an image file that is used in the gui.

6. **bartimaeus_db.sql:**
       This is the on-disk db for the program created using sqlite3, it contains entries that I used to test the application. You don't need to use this as you can initialise a new one when you run bartimaeus_gui_main.py. If you would rather use MS SQL Server, make sure to do the necessary adjustments to the bartimaeus_gui_main.py and bartimaeus_db.py files. I can't entirely tell what changes need to be made but you can scan through the aforementioned two files, inspect the queries and work with any errors you get to make the required changes.

