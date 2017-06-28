from os.path import dirname
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'Imran'

LOGGER = getLogger(__name__)


class ResponseTestSkill(MycroftSkill):
    def __init__(self):
        super(ResponseTestSkill, self).__init__(name="ResponseTest")
        self.ask = False
        self.ask_1=False

    def initialize(self):
        
        introduction_intent = IntentBuilder('IntroductionIntent'). \
            require("IntroductionKeyword").build()
        askingname_intent = IntentBuilder('AskingNameIntent'). \
            require("AskingNameKeyword").optionally("name").build()
        askingphone_intent = IntentBuilder('AskingPhoneIntent'). \
            require("AskingPhoneKeyword").build()
 
 
        self.register_intent(introduction_intent, self.handle_introduction_intent)
        self.register_intent(askingname_intent, self.handle_askingname_intent)
        self.register_intent(askingphone_intent, self.handle_askingphone_intent)


      #everytime a utterance message is heard from wherever (cli, voice, etc)
      #call save_utterance method
	self.emitter.on("recognizer_loop:utterance", self.save_utterance)


    #To activate this say Hey Mycroft I am here to give feedback
    def handle_introduction_intent(self, message):
        self.ask = True
        self.speak_dialog("Introduction",
                   expect_response=True)    

    #To activite this say Imran
    def handle_askingname_intent(self, message):
        if self.ask:
            Name = message.data.get("name")
            self.speak_dialog("AskingName", {"Name": Name})
            self.ask_1 = True
            self.ask = False
            
   

    #Activate this say handphone no
    def handle_askingphone_intent(self, message):
        if self.ask_1:
            self.speak_dialog("AskingPhone")
            self.ask_1 = False
            with open("dirname(__file__) + "/input.txt", "wb") as f:
                f.write("Hello")

    
  
	

##    def save_utterance(self, message):
##	#utterance = message.data.get("utterance")
##	# do whatever you want with it
##	#sentiment = self.sentiment_analisys(utterance)
##	# save it
##	f = open("/home/pi/downloads/inputs.txt", "w")
##	f.write("Hello")
##	f.close()

    # handle special cases
    
##    utterance = message.data.get("utterance");
##    # if no intent inside this skill will trigger
##    if id != self.skill_id:
##        words = utterance.split(" ")
##            size = len(words)
##            if size == 1:
##            # name is this word maybe
##            name = words[0]
##            # call intent directly, add name to params (regex variable name)
##            self.handle_intent({"name":name})
##                return True
##    return False

    


def create_skill():
    return ResponseTestSkill()
