##Adding Radio Stations

Once you have the URL of the radio station

1. Open config.json.template file from the skills folder
2. Add the URL to the "values" list in the following form

Example format...

``
"values": {
			"The speakable name of the Station": "the station URL"
			}
``	
		
Proper example:

``
"values": {
			"Jazz": "http://theJazzStationURL",
			"eighties Music": "http://80sMusicUrl",
			"B B C": "http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk"
			}
``			

##Functionality of the skill

You can ask Alice variations of the below :

- Play the B B C radio 
- Play station number 3

Changing between stations can be done by :

1. speaking - play the "newStationName" radio
2. Selecting it from thedrop down list in the skill settings
3. speaking - play station number "then the number". This will play what ever line number you've choosen 

When alice understads what station you want to play she will

- mpc clear
- mpc add
- mpc play

To stop playing you'll have to use something like NR or command line.

By changing station via any of the above methods, Alice will write the listed names from the config.json.template file
to the dialogTemplate slot's so you can request that radio station. She'll do this when you 

1. click save in the skill settings
2. Request a different station from the current one

So. If you add new URl's or update the speakable names in the config.json.template file, open the skill settings
and click "save" that'll update the slots in dialogTemplate
