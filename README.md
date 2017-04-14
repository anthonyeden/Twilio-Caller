# [Twilio Caller](https://mediarealm.com.au/articles/2017/04/offair-alarm-phone-caller-twilio/)
A simple utility to trigger outgoing phone calls via Twilio. Designed for radio station Program Fail / Dead Air alarms.

![Automatic Calls with Twilio](https://mediarealm.com.au/wp-content/uploads/2017/04/Twilio-Dead-Air-Caller-PFA.jpg)

This utility uses Twilio’s Programmable Voice service as an inexpensive way of triggering phone calls via an API. It's designed to work with Broadcast Silence Detection software such as [Pira.CZ](http://pira.cz/show.asp?art=silence) and [Pathfinder](http://www.pathfinderpc.com).

## Startup options:

You can start this application using any of these command line parameters:

	--call=+61288063416 (the number to send the call to - full international format)
	--from=+61288063416 (the number to originate the call from - must be registered in Twilio)
	--message="Your radio station is off the air." (the message to read out)
	--messagerepeat=2

The options "call" and "message" are mandatory. The options "from" and "messagerepeat" can also be set in the __config.json__ file, but specifying them on startup will override the defaults.

## Setup Instructions:

A detailed setup guide is available on the Media Realm website: [Automatic Off-Air Phone Calls with Twilio: Get a call when you're off-the-air](https://mediarealm.com.au/articles/2017/04/offair-alarm-phone-caller-twilio/).

## Not working? Want to help?

Feel free to log issues or create pull requests in GitHub.

## License:

Copyright 2017 Anthony Eden

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
