"""
Media Realm's Twilio Caller

This script is designed to call a phone number via Twilio and read out a message.
Designed for Program Fail Alarms for radio stations.

Startup options:
	--call=+61288063416 (the number to send the call to - full international format)
	--from=+61288063416 (the number to originate the call from - must be registered in Twilio)
	--message="Your radio station is off the air." (the message to read out)
	--messagerepeat=2

Developed by Anthony Eden (http://mediarealm.com.au/)
"""

import os
import sys
import json
import logging
import logging.handlers
import urllib

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/libs")

from xml.sax.saxutils import escape
from twilio.rest import TwilioRestClient

def setupLogging():
	# Enable Logging:
	logging_filename = os.path.join(os.path.dirname(sys.executable), "TwilioCaller.log")

	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)

	handler = logging.handlers.RotatingFileHandler(logging_filename, maxBytes = 104857600, backupCount = 5)
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt = '%Y-%m-%d %I:%M:%S %p')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	handler_print = logging.StreamHandler(sys.stdout)
	handler_print.setLevel(logging.DEBUG)
	handler_print.setFormatter(formatter)
	logger.addHandler(handler_print)

	# Stop it double-saving to the text file
	logger.propagate = False

	logging.basicConfig(
		filename = logging_filename,
		level = logging.DEBUG,
		format = '%(asctime)s %(levelname)s:     %(message)s',
		datefmt = '%m/%d/%Y %I:%M:%S %p')

	return logger

def setupConfigFile():
	try:
		ConfigData_JSON = open(os.path.join(os.path.dirname(sys.executable), "config.json")).read()
		ConfigData = json.loads(ConfigData_JSON)
		
		logger.info("Config file JSON has been opened and parsed")

	except Exception, e:
		logger.exception("JSON Config file could not be parsed")
		sys.exit()
	
	return ConfigData

def setupTwilioClient():

	if "TwilioAccountSID" in ConfigData and "TwilioAuthToken" in ConfigData:
		# Get these credentials from http://twilio.com/user/account
		try:
			return TwilioRestClient(
				ConfigData["TwilioAccountSID"],
				ConfigData["TwilioAuthToken"]
			)
		except Exception, e:
			logger.exception("Error connecting to Twilio. Check your credentials and internet connection.")
			sys.exit()
	
	else:
		logger.error("Options not found in Config File: TwilioAccountSID and/or TwilioAuthToken")
		sys.exit()

def buildTwimML(callMessage, callMessageRepeatTimes, callMessageGoodbye):
	TwiML = "<Response>"
	
	for i in range(0, callMessageRepeatTimes):
		TwiML += """
				<Say voice="woman">
					""" + escape(callMessage) + """
				</Say>
				<Pause length="3"></Pause>"""
	
	TwiML += """
		<Say voice="man">
			""" + escape(callMessageGoodbye) + """
		</Say>
		<Pause length="2"></Pause>"""
	
	TwiML += "</Response>"

	return TwiML

def placeCall(number, callFrom, TwiML):
	# Method to place the call with Twilio

	try:
		call = client.calls.create(
			to = number,
			from_ = callFrom,
			url = "http://twimlets.com/echo?" + urllib.urlencode({"Twiml": TwiML}))

		logger.info("Call Triggered to " + str(number) + " with Twilio SID " + str(call.sid))
		return True

	except Exception, e:
		logger.exception("Error placing call with Twilio. Check your credentials, internet connection, and phone number formatting")
		return False

if __name__ == "__main__":
	
	logger = setupLogging()
	logger.info("Media Realm Twilio Caller has started")

	ConfigData = setupConfigFile()
	client = setupTwilioClient()

	if "CallFrom" in ConfigData:
		callFrom = ConfigData["CallFrom"]
	else:
		callFrom = None
	
	# How many times should the message be read out?
	if "MessageRepeatTimes" in ConfigData:
		callMessageRepeatTimes = int(ConfigData["MessageRepeatTimes"])
	else:
		callMessageRepeatTimes = 2
	
	# A final message that gets appended to every call (in a different voice)
	if "GoodbyeMessage" in ConfigData:
		callMessageGoodbye = ConfigData["GoodbyeMessage"]
	else:
		callMessageGoodbye = "This has been an automated call, powered by Twilio and Media Realm. Goodbye."
	
	# These options don't have default values and must be set in the args
	callNumber = None
	callMessage = None

	for arg in sys.argv:
		if arg[:7] == "--call=":
			callNumber = arg[7:]
		if arg[:10] == "--from=":
			callFrom = arg[7:]
		if arg[:10] == "--message=":
			callMessage = arg[10:]
		if arg[:16] == "--messagerepeat=":
			callMessageRepeatTimes = arg[16:]
	
	if callFrom is None or callNumber is None or callMessage is None:
		logger.error("You must specify some startup arguments")
		logger.error("--call=+61411222333 --message=\"Read this out\"  --from=+61211112222")
		sys.exit()
	
	# Build the XML
	TwiML = buildTwimML(callMessage, callMessageRepeatTimes, callMessageGoodbye)

	# Multiple numbers can be separated by a comma
	callNumbers = callNumber.split(",")
	callSuccessCount = 0
	logger.info("There are " + str(len(callNumbers)) + " number(s) to call")

	# Loop over all the numbers and trigger the calls:
	for number in callNumbers:
		if placeCall(number, callFrom, TwiML):
			callSuccessCount += 1
	
	# Log how many calls were placed
	if callSuccessCount == 1:
		logger.info(str(callSuccessCount) + " call has been sent to Twilio.")
	else:
		logger.info(str(callSuccessCount) + " calls have been sent to Twilio.")
	
	# End of the script.
	logger.info("Script has ended. It was powered by http://mediarealm.com.au/ and http://twilio.com/.")

