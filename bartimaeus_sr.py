import pyttsx3   
import time
import speech_recognition as sr 
from bartimaeus_db import Database
from bartimaeus_email import send_email
from datetime import datetime 
from dateutil import parser
import sys
import re




#------------------------------defining required functions--------------------------------

#this is the tts engine. Also updates the console section of the gui
def speak(GUI,text):
    engine = pyttsx3.init()
    # Function to convert text to speech
    GUI.console_entry.delete('0.0','end')
    GUI.console_entry.insert('0.0',text)
    engine.say(text)
    engine.runAndWait()
    GUI.console_entry.delete('0.0','end')

#updates the console section of the gui, used to update the user on the programs 
#processes when tts is not required
def gui_prompt_display(GUI,prompt):
    GUI.console_entry.delete('0.0','end')
    GUI.console_entry.insert('0.0',prompt)

# this runs when the program is completed or when the user says quit
def quit_clean_up(GUI):
        GUI.name_entry.delete('0','end')
        GUI.email_entry.delete('0','end')
        GUI.subject_entry.delete('0','end')
        GUI.message_entry.delete('0.0','end')
        GUI.console_entry.insert('0.0','The program has ended, you can now close this window or restart the program by clicking the Compose button')
        
    
    
    
# this is the sr engine, rarely called by itself. 
# it is usually called by another function -> voice_statement_validation
def listen(GUI):
    r = sr.Recognizer()
    # Function to listen to user's voice input
    with sr.Microphone() as source:
        gui_prompt_display(GUI,'Listening...')
        print("Listening...")
        audio = r.listen(source)

    try:
        gui_prompt_display(GUI,'Recognizing...')
        print("Recognizing...")
        text = r.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
        return None

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        speak(GUI,'The program needs an internet connection, but no internet connection is detected, please connect to the internet and try again. The program will end now. Goodbye')
        quit_clean_up(GUI)
        sys.exit()


#this is used to listen to and validate user input
#calls two other functions depending on the input validation that needs to be done
def voice_statement_validation(GUI,content_type:str,func,*args):
    try:
        if func == statement_validation:
            while True:   
                presumed_input = listen(GUI)
                if presumed_input:
                    if 'quit' == presumed_input.lower():
                        prompt = 'Confirmed, you said quit. The program will end now. Goodbye'
                        speak(GUI,prompt)
                        quit_clean_up(GUI)
                        sys.exit()
                    else:
                        message = 'Did you say ' + presumed_input +'?'
                        return func(GUI,presumed_input,message,content_type)           
                else:
                        speak(GUI,f"Sorry, I didn't catch that. Please say the {content_type} again")
        elif func == yes_no_validation:
            message_yes, message_no = args
            while True:   
                presumed_input = listen(GUI)
                if presumed_input:
                    if 'quit' == presumed_input.lower():
                            prompt = 'Confirmed, you said quit. The program will end now. Goodbye'
                            speak(GUI,prompt)
                            quit_clean_up(GUI)
                            sys.exit()
                    else:
                        return func(GUI,presumed_input,message_yes,message_no)           
                else:   
                        prompt = f"Sorry, I didn't catch that. Please say the {content_type} again"
                        speak(GUI,prompt)
    except Exception as e:
        speak(GUI,'Oh no, there has been an unexpected problem, the program will end now, please try running the program again. Goodbye')
        quit_clean_up(GUI)
        print(e)
        exit()    

# used to confirm only yes and no input from the user
def yes_no_validation(GUI,presumed_input,message_yes,message_no,keep_running = True):
    try:
        while True:
            if not keep_running:
                return presumed_input
            else:
                def inner_yes_no_validation(GUI,presumed_input):
                    if 'yes' == presumed_input.lower():
                        prompt = 'Confirmed, you said yes'
                        speak(GUI,prompt)
                        speak(GUI,message_yes) 
                        keep_running = False
                        return 'yes', keep_running
                    
                    elif 'no' == presumed_input.lower():
                        prompt = 'Confirmed, you said no'
                        speak(GUI,prompt)
                        speak(GUI,message_no)
                        keep_running = False
                        return 'no', keep_running
                    
                    elif 'quit' == presumed_input.lower():
                        prompt = 'Confirmed, you said quit. The program will end now. Goodbye'
                        speak(GUI,prompt)
                        quit_clean_up(GUI)
                        exit()
                    else:
                        prompt = 'I\'m not sure if you said yes or no, please say again'
                        speak(GUI,prompt)
                        keep_running = True
                        presumed_input = listen(GUI)
                        return presumed_input, keep_running
                presumed_input, keep_running = inner_yes_no_validation(GUI,presumed_input)
    except Exception as e:
        prompt = 'Oh no, there has been an unexpected problem, the program will end now, please try running the program again. Goodbye'
        speak(GUI,prompt)
        quit_clean_up(GUI)
        print(e)
        exit()


#used to confirm content input e.g. name,email body. Also does yes/no validation for the content
def statement_validation(GUI,presumed_input,message,content_type,keep_running=True):
    try:
        while True:
            if not keep_running:
                return presumed_input
            else: 
                speak(GUI,message)
                validate_input = listen(GUI)

                
                def inner_statement_validation(GUI,presumed_input,validate_input,content_type): 
                    
                    if validate_input:
                        if 'yes' == validate_input.lower():
                            keep_running = False
                            message = ''
                            speak(GUI,'Confirmed, you said '+ presumed_input)
                            return presumed_input, keep_running, message
                        
                        
                        elif 'no' == validate_input.lower():                     
                            message = f"oh no, sorry for the mistake. Please say the {content_type} again"
                            keep_running = True
                            presumed_input = ''                         
                            return presumed_input, keep_running, message
                        
                        elif 'quit' == validate_input.lower():
                            speak(GUI,'Confirmed, you said quit. The program will end now. Goodbye')
                            quit_clean_up(GUI)
                            exit()    
                    
                        elif 'no' not in validate_input and 'yes' not in validate_input:                           
                            message = 'Did you say '+ validate_input
                            keep_running = True
                            return validate_input, keep_running, message
                                             
                        else:
                            message = 'I\'m not sure if you said yes or no, please say again'
                            keep_running = True
                            return validate_input, keep_running, message

                    else :
                        message = 'I\'m not sure what you said, please say again'
                        keep_running = True
                        return presumed_input, keep_running, message
                    
                presumed_input,keep_running,message =  inner_statement_validation(GUI,presumed_input,validate_input,content_type)#,name
                    
    except Exception as e:
        speak(GUI,'Oh no, there has been an unexpected problem, the program will end now, please try running the program again. Goodbye')
        print(e)
        quit_clean_up(GUI)
        exit()        


#this is where the program starts from, it is imported by bartimaeus_gui_main.py
def start_program(GUI):
    GUI.console_entry.delete('0.0','end')
    GUI.console_entry.insert('0.0','Starting program ...')

    db = Database()
    db.connect()

    time.sleep(2)

    prompt = "Hello, hope you are doing well. Remember, you can always say quit, anytime you want to end the program and the program will be terminated. I see you will like to send a message. Who would you like to message today?"
    speak(GUI,prompt)
    recipient_name = voice_statement_validation(GUI,'name',statement_validation)
    GUI.name_entry.insert('0',recipient_name)


    last_email = db.read_email_history(recipient_name,'bartimaeusEmailHistory')

    if not isinstance(last_email,tuple):
        speak(GUI,last_email)
        run_rest_of_program(GUI,db,recipient_name)
    else:
        idd,recipient_email,name,email_subject,email_message,status,send_time = last_email
        send_time = parser.parse(send_time)
        day = send_time.strftime('%d')
        month = send_time.strftime('%B')
        days_diff = datetime.today() - send_time

        if days_diff.days > 1 :
            diff_message = f'{days_diff.days} days ago on the {day} of {month}'
        else:
            diff_message = f'less than a day ago'
        time.sleep(1)
        speak(GUI,f'You last sent an email to {name.title()} {diff_message}, would you like to repeat your last sent message? ')
    
        message_yes = f'Your last email to {recipient_name} will be sent'
        message_no = f'Your last email to {recipient_name} will not be sent. You will now need to provide the subject and body for the email you want to send'
    
        send_previous_email = voice_statement_validation(GUI,'response',yes_no_validation,message_yes,message_no)


        if 'yes' in send_previous_email.lower():
            speak(GUI,f'The subject of the last email is: {email_subject.title()}. And the body is: {email_message.capitalize()}. Would you still like to send this message?')
            message_yes = f'Your last email to {recipient_name} will now be sent'
            message_no = f'Your last email to {recipient_name} will no longer be sent. You will now need to provide the subject and body for the email you want to send'
            go_ahead = voice_statement_validation(GUI,'response',yes_no_validation,message_yes,message_no)


            if 'yes' in go_ahead.lower():
                GUI.email_entry.insert('0',recipient_email)
                GUI.subject_entry.insert('0',email_subject.title())
                GUI.message_entry.insert('0.0',email_message.title())       
                is_successful = send_email_with_validation(GUI,recipient_name,email_message,email_subject,recipient_email)
                save_email_message(GUI,db,is_successful,recipient_email,recipient_name,email_subject,email_message)
                                
            elif 'no' in go_ahead.lower():
                run_rest_of_program(GUI,db,recipient_name)
        elif 'no' in send_previous_email.lower():
            run_rest_of_program(GUI,db,recipient_name)

    time.sleep(1)

    speak(GUI,"Thank you for using Bartimeus, I hope it was not a hassle using the program. If you have any feedback about the program, please send your feedback to Dami, or Tamara, or Timothy, or Tuyo. Make sure you do not contact Oye. Oye no like wahala. See you next time Steve, do enjoy the rest of your day. Goodbye")
    time.sleep(1)
    quit_clean_up(GUI)
    





# used to save the email address for a new recipient
def save_email_address(GUI,db,recipient_name):
    time.sleep(1)
    speak(GUI,f'What is {recipient_name}\'s email address?')
    recipient_email = voice_statement_validation(GUI,'email address',statement_validation)
    recipient_email = re.sub('at','@',recipient_email)
    recipient_email = re.sub('\s+','',recipient_email) 

    gui_prompt_display(GUI,recipient_email)
    
    # current implementation will keep re-trying to save the email address forever if the saving is failing
    # it could be adjusted to stop trying after a number of attempts
    while True:
        success = db.insert_data('bartimaeusContactList',f"'{recipient_name.title()}','{recipient_email}'")
        if success :
            speak(GUI,'The email has been successfully added to your contact list, you can now proceed with sending the email')
            return recipient_email
        else :
            speak(GUI,'The email was not successfully added to your contact list, trying again')
            continue


# Used to send out emails
def send_email_with_validation(GUI,recipient_name,email_body,email_subject,recipient_email):
    gui_prompt_display(GUI,'Sending email ...')
    
    is_successful = send_email(email_body,email_subject,recipient_email)
    if is_successful:
        speak(GUI,f"The email has been sent successfully. I\'m sure {recipient_name} would be glad to receive your email")
    else:
        speak(GUI,f"The email was not successfully sent. I\'ll try to send the email again now.")
        gui_prompt_display(GUI,'Sending email ...')
        
        is_successful = send_email(email_body,email_subject,recipient_email)
        if is_successful:
            speak(GUI,f"The email has now been sent successfully. I\'m sure {recipient_name} would be glad to receive your email")
        else:
            speak(GUI,f"The email was still not able to send, this might be due to a network problem, but don't worry, i\'ll save the email in your outbox so you can try sending it later. Sorry for the troubles")
            
    return is_successful

def save_email_message(GUI,db,is_successful,recipient_email,recipient_name,email_subject,email_message):
    gui_prompt_display(GUI,'Saving email ...')
    
    # This block needs some work to handle failed data insertion
    # current implementation will show successful, even when insertion failed 
    if is_successful:
        sql_query = f"'{recipient_email}','{recipient_name}','{email_subject}','{email_message}','sent'"
        
        db.insert_data("bartimaeusEmailHistory",sql_query)
        speak(GUI,"The email has also been saved in your email history. You can access the email whenever you want")
    else:
        sql_query = f"'{recipient_email}','{recipient_name}','{email_subject}','{email_message}','notsent'"
        
        db.insert_data("bartimaeusEmailHistory",sql_query)
        speak(GUI,"The email has been saved in your email history. You can access the email whenever you want")
    

#section where email subject and body is received 
def run_rest_of_program(GUI,db,recipient_name):
    time.sleep(1)

    recipient_email = db.read_email(recipient_name,"bartimaeusContactList")
    if not recipient_email:
        speak(GUI,f'I could not retrieve an email address for {recipient_name}, because it has not been saved in your contacts list. Would you like to save {recipient_name}\'s email address?')
        message_yes = 'The email address will now be saved'
        message_no = ''
        ans = voice_statement_validation(GUI,'response',yes_no_validation,message_yes,message_no)
        if 'yes' in ans:
           recipient_email = save_email_address(GUI,db,recipient_name)
        elif 'no' in ans:
            message_yes = 'The email address will now be saved'
            message_no = 'Since you did not save the email address, the program will terminate now. Goodbye'
            speak(GUI,f'You will not be able to send an email to {recipient_name} if you do not save their email address. Would you now like to save {recipient_name}\'s email address? Please note, if you say no, the program will be terminated')
            ans = voice_statement_validation(GUI,'response',yes_no_validation,message_yes,message_no)
            if 'yes' in ans:
              recipient_email = save_email_address(GUI,db,recipient_name)
            elif 'no in ans' :
                time.sleep(1)
                quit_clean_up(GUI)
                exit()
    else:
        recipient_email = recipient_email[0]
        speak(GUI,f'I have successfully retrieved {recipient_name}\'s email address from your contact list. You can now provide the subject and body for the email you want to send')


    GUI.email_entry.insert('0',recipient_email)

    time.sleep(1)

    # getting email subject
    speak(GUI,"What would you like the subject of the email to be?")
    email_subject = voice_statement_validation(GUI,'email subject',statement_validation)
    
    GUI.subject_entry.insert('0',email_subject.title())
    speak(GUI,"Email subject Received")

    time.sleep(1)

    # getting email body
    speak(GUI,f"What message would you like to send to {recipient_name}")
    email_body = voice_statement_validation(GUI,'email body', statement_validation)
    
    GUI.message_entry.insert('0.0',email_body.title())
    speak(GUI,"Email body Received")


    time.sleep(1)

    # sending email out
    speak(GUI,f"All the email content have now been received, would you like to send the email to {recipient_name} now?")
    message_yes= 'The email will be sent'
    message_no = 'Since you do not want to send the email now, it will be saved in case you want to send it later.'
    answer = voice_statement_validation(GUI,'response',yes_no_validation,message_yes,message_no)

    # current implementation auto saves unsent emails, 
    # could be adjusted to ask the user if it should be saved or deleted
    if 'yes' in answer.lower():
        
        is_successful = send_email_with_validation(GUI,recipient_name,email_body,email_subject,recipient_email)
        save_email_message(GUI,db,is_successful,recipient_email,recipient_name,email_subject,email_body)
        
    elif 'no' in answer.lower():
        is_successful = 0 
        
        save_email_message(GUI,db,is_successful,recipient_email,recipient_name,email_subject,email_body)


#------------------------------------------------------------------------------------
