from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import smtplib


__author__ = 'Imran'

LOGGER = getLogger(__name__)


class ResponseTestSkill(MycroftSkill):
    def __init__(self):
        super(ResponseTestSkill, self).__init__(name="ResponseTest")
        self.ask = False
        self.ask_1=False
        self.ask_2= False
        self.ask_Introduction = True

    def initialize(self):
        
        introduction_intent = IntentBuilder('IntroductionIntent'). \
            require("IntroductionKeyword").build()
        askingname_intent = IntentBuilder('AskingNameIntent'). \
            require("AskingNameKeyword").optionally("Name").build()
        askingphone_intent = IntentBuilder('AskingPhoneIntent'). \
            require("AskingPhoneKeyword").optionally("Phone").build()
        askingfeedback_intent = IntentBuilder('FeedbackIntent'). \
            require("FeedbackKeyword").optionally("Feedback").build()
 
 
        self.register_intent(introduction_intent, self.handle_introduction_intent)
        self.register_intent(askingname_intent, self.handle_askingname_intent)
        self.register_intent(askingphone_intent, self.handle_askingphone_intent)
        self.register_intent(askingfeedback_intent, self.handle_askingfeedback_intent)



   


    #To activate this say Hey Mycroft I am here to give feedback
    def handle_introduction_intent(self, message):
        if self.ask_Introduction:
            self.ask=True
            self.speak_dialog("Introduction",
                   expect_response=True)    
            self.ask_Introduction= False
            
    #To activite this say name or here
    def handle_askingname_intent(self, message):
        if self.ask:
            name = message.data.get("Name")
            self.speak_dialog("AskingName", {"name": name})
            self.ask_1 = True
            self.ask = False

            with open("/home/pi/downloads/input.txt","w") as f:
                f.write(name)

 
    #Activate this say handphonenumber is
    def handle_askingphone_intent(self, message):
        if self.ask_1:
            phone = message.data.get("Phone")
            self.speak_dialog("AskingPhone", {"phone": phone})
            self.ask_1 = False
            self.ask_2 = True

       

            with open("/home/pi/downloads/input.txt","r") as f:
                feedback_user=f.read()

            

            email_name = "Name is " + feedback_user
            email_content= "\nHandphone Number is " + phone
            
            server=smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login("","")
            server.sendmail("","", email_name + email_content)
            server.quit()

    def handle_askingfeedback_intent(self,message):
        if self.ask_2:
            feedback = message.data.get("Feedback")
            self.speak("Working")
            self.ask_2= False
       

    def stop(self):
        pass

                
def create_skill():
    return ResponseTestSkill()
