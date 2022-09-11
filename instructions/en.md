## About the skill

This skill is a simple radio player that plays stations that are configured in the config.json.template file.
You can add and remove stations to suit your taste. Please see below details.

This skill comes with a several Stations to choose from already. You can add your own if required as per below

- TIP: If your looking for a more advanced radio skill, try [Nepos MultiRoom Radio skill](https://github.com/poulsp/skill_MultiRoomRadioManager/blob/master/instructions/en.md)


## Adding your own Radio Stations

Find the URL of your favorite Internet based radio station. Once you have the URL ...

1. Open config.json.template file from the skills folder
2. Add the URL to the "values" list in the following form

*Example format...*


"values": {
			"The speakable name of the Station": "the station URL"
			}

	
*Proper example:*


"values": {
			"Jazz": "http://theJazzStationURL.pls",
			"eighties Music": "http://80sMusicUrl.m3u",
			"B B C": "http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk"
			}

			
### The station URL can be in the following streaming formats:


- *.pls URLS
- *.m3u URLS
- Direct streaming links

NOTE :  *.m3u8 URLS currently not supported

## Functionality of the skill

To play the radio

* Ask Alice variations of :
- Play the B B C radio 
- Play station number 3

* Or from the skill settings :
- Selecting a different station in the dop down list will automatically play that station
- Enabling "turn on the radio" in the skill settings will play the current listed station

Changing between stations can be done by :

1. saying -> play the "newStationName" radio
2. Selecting it from the drop-down list in the skill settings
3. saying -> play station number "then the number". This will play what ever line number you've choosen 

NOTE: Intents aim to have the word "radio" in them so that the intent is less likely to
clash when someone makes a spotify or some other music skill.

## Stopping the radio
Depending on your speaker volume, it is possible that Alice may not hear or understand you if you ask her to "Stop the radio"

In this situation you have a few options to turn the radio off. Below i've listed some of the easy options.

1. Type "stop the radio" in Alices dialog view
2. Open the skills settings and turn on the "stop the radio" toggle.
3. Type "mpc stop" in the command line


## Let's talk about Back-up files
For the back-up option to work you need to enable it in the settings and turn "Dev mode" on in alice's settings.
Without Dev mode on and left on, Alice is likely to put the skill back to default values when she cleans her house, 
meaning you'll probably lose any custom radio stations you might have added.


The skill backs up your stations to a Backup directory. The files being backed up are the dialogTemplate file 
and the config.json.template file. If you modify the config.json.template manually, upon next Alice restart she 
will do a backup.

So. If you add new URl's or update the speakable names in the config.json.template file, Alice will

- Write the station names to the dialogTemplate file as values
- Then she'll do a back-up of the above two files
- You'll then need to re-train her or restart her to trigger training

- NOTE: My advice would be to enable the "enable Backup" toggle in the skill settings only when you make changes to the
config.json.template file, reboot and let her retrain. Then disable it again.
	
  - Reason being : If the skill gets updated.... the template file is a main file so it "might" get overwritten which 
  will trigger a back-up command (if enabled) on re boot, which in turn would over write your existing back-up file with
  the standard diaolg file and config file... defeating the purpose of a back-up file :)

The back-up files are there to manually copy and overwrite existing files if the skill gets updated and/or you lose
your custom list of stations for what ever reason. This feature, although called back-up, was added purely to save you
adding values to the dialog file manually. Just so happens it can also be used as a back-up :)
