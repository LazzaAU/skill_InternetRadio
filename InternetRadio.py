import json
import re
import urllib

#from skills.AliceDevTools import AliceDevTools
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from pathlib import Path
from urllib.request import urlopen


class InternetRadio(AliceSkill):
	"""
	Author: lazzaAU
	Description: Listen to internet radio stations
	"""

	def __init__(self):

		self._templatePath = '/InternetRadio/config.json.template'
		self._selectedStation = ""
		self._data = dict()
		self._backupPath = ""
		self.playlist = list()
		#AliceDev used for internal developer use
		#self.AliceDev = AliceDevTools.AliceDevTools()

		super().__init__()

	@IntentHandler('StopPlayingRadio')
	def StopRadio(self, session: DialogSession):
		"""
		Used for stopping music playing. In general this may not work due to alice's
		speaker running already. However, still triggers from dialog view in the GUI
		:param session: the dialog session
		:return:
		"""
		if 'StopTheRadio' in session.slotsAsObjects:
			self.Commons.runSystemCommand(f'mpc stop '.split())
			self.Commons.runSystemCommand(f'mpc clear '.split())
			if self.getConfig('startPlaying'):
				self.updateConfig(key='startPlaying', value=False)

		self.endDialog(
			sessionId=session.sessionId,
			text=self.randomTalk(text="dialogMessage4"),
			deviceUid=session.deviceUid
		)

	@IntentHandler("ListenToRadio")
	def setupTheStation(self, session: DialogSession, **_kwargs):
		# Read the config.json.template file to get the list of values
		self._data = self.readTemplateData(configPath=self.getResource('config.json.template'))

		# If user has not specified a station, just play the default station
		if not 'RadioStation' in session.slotsAsObjects and not 'number' in session.slotsAsObjects:
			self.stationSelected(station=self.getConfig(key='radioStations'))

			self.endDialog(
				sessionId=session.sessionId,
				text=self.randomTalk(text="dialogMessage4"),
				deviceUid=session.deviceUid
			)
			return

		# If user specified the station, match it up to the url
		# if user specified a number, select that line from the list if available
		if session.slotValue('number'):
			listLength = len(self._data)
			number: int = session.slotValue('number')

			# if user asks for list number that doesn't exist
			if number > listLength:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text="dialogMessage1", replace=[number, listLength +1]),
					deviceUid=session.deviceUid
				)
				return
			else:
				counter = 1
				for item in self._data:
					# update the config with selected url via number selection
					if counter == number:
						self._selectedStation = self._data.get(item)
						self.updateConfig(key='radioStations', value=self._selectedStation)
						self.endDialog(
							sessionId=session.sessionId,
							text=self.randomTalk(text="dialogMessage4"),
							deviceUid=session.deviceUid
						)
						self.stationSelected(station=self._selectedStation)
						return
					counter += 1

		choosenStation = session.slotValue('RadioStation')

		for key in self._data:
			# update the config with choosen station via station name
			if key in choosenStation:
				# Find the requested station
				self._selectedStation = self._data.get(key)
				self.updateConfig(key='radioStations', value=self._selectedStation)
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text="dialogMessage4"),
					deviceUid=session.deviceUid
				)
				self.stationSelected(station=self._selectedStation)
				return
		else:
			self.endDialog(
				sessionId=session.sessionId,
				text=self.randomTalk(text="dialogMessage2"),
				deviceUid=session.deviceUid
			)

	def stopPlaying(self, value):

		if value:
			self.Commons.runSystemCommand(f'mpc stop '.split())
			self.Commons.runSystemCommand(f'mpc clear '.split())

			self.ThreadManager.doLater(
				interval=4,
				func=self.delayedConfigUpdate,
				args=[
					'stopPlaying',
					False
				]
			)
			if self.getConfig('startPlaying'):
				self.ThreadManager.doLater(
					interval=5,
					func=self.delayedConfigUpdate,
					args=[
						'startPlaying',
						False
					]
				)
			self.say(
				text=self.randomTalk(text="dialogMessage5")
			)

		return True

	def delayedConfigUpdate(self, key :str, value : bool):
		"""
		Required function to update the config on a timer after a onUpdate event
		"""
		self.updateConfig(key=key, value=value)


	def startPlaying(self, value):
		if value:
			self.stationSelected(station=self.getConfig('radioStations'))
			self.ThreadManager.doLater(
				interval=5,
				func=self.delayedConfigUpdate,
				args=[
					'stopPlaying',
					False
				]
			)
		return True

	def stationSelected(self, station: str, session = None):
		"""
		When the user clicks the "confirm" button on the skill settings after selecting a station, or by verbally
		Then parse the Url and play the selected Station, or stop the player if that toggle is enabled
		:return:
		"""
		self.parsePlaylists(stationUrl=station)
		if self.playlist or self._selectedStation:
			self.runThePlayer()

		if session:
			self.endDialog(
				sessionId=session.sessionId,
				text=self.randomTalk(text="dialogMessage3")
			)
		return True


	@staticmethod
	def readTemplateData(configPath : Path):
		"""
		Read and store the template list
		:return: dictionary of just the radio station list
		"""

		data = json.loads(configPath.read_text())
		tempData = dict()

		# Trim the original json to just the relevant values
		for key in data['radioStations']['values']:
			tempData[key] = data['radioStations']['values'][key]

		return tempData


	def runThePlayer(self):
		"""
		Commands to run the actual player
		:return:
		"""
		self.Commons.runSystemCommand(f'mpc stop '.split())
		self.Commons.runSystemCommand(f'mpc clear '.split())

		if self.playlist:
			urlPlaying = self.playlist[0]
			for item in self.playlist:
				self.Commons.runSystemCommand(f'mpc add {item}'.split())
		else:
			urlPlaying = self._selectedStation
			self.Commons.runSystemCommand(f'mpc add {self._selectedStation}'.split())

		result = self.Commons.runSystemCommand(f'mpc play'.split())

		if self.getConfig(key='debugMode'):
			status = self.Commons.runSystemCommand(f'mpc status'.split())
			currentPlaylist = self.Commons.runSystemCommand(f'mpc playlist'.split())
			self.logDebug(f"MPC status is {status}")
			self.logWarning("--")
			self.logDebug(f"Current playlist is {currentPlaylist}")
			self.logWarning("--")

		if not result.returncode:
			self.logInfo(f'Playing Radio Station from *** {urlPlaying} ***')

		else:
			self.logWarning(f"Failed to play due to {result.stderr}")

		self._selectedStation = ""
		self.playlist = list()

	def addSlotValues(self) -> bool:
		"""
		Update the dialogTemplate file with new slotvalues based on config.json.template
		Then copy that file to the backup folder
		:return:
		"""
		file = self.getResource(f'dialogTemplate/{self.activeLanguage()}.json')

		if not file:
			return False
		# load the dialogTemplate file data
		data = json.loads(file.read_text())

		slotValue = list()

		# Set up the slot values
		for item in self._data:
			tempData = {'value': item, 'synonyms': []}

			slotValue.append(tempData)

		# Add slot values to the dialogTemplate slotType
		for i, suggestedSlot in enumerate(data['slotTypes']):
			if "radiostation" in suggestedSlot['name'].lower():
				data['slotTypes'][i]['values'] = slotValue

		file.write_text(json.dumps(data, ensure_ascii=False, indent=4))
		self.logInfo(f"Radio files have been backed up, please retrain or restart Alice")

		# Make a backup of the file , so user can back up settings if needed
		self.Commons.runSystemCommand(['cp', file, self.getResource(f'Backup/dialogTemplate/{self.activeLanguage()}.json') ])
		return True

	def BackupPathRoutines(self):
		"""
		Make backup directories if they don't exist. Then Backup the config.template file
		if it's not the same as existing backup
		:return:
		"""

		self._data = self.readTemplateData(configPath=self.getResource('config.json.template'))
		if not self.getResource('Backup').exists():
			self.logWarning(f'No BackUp directory found, so I\'m making one')
			self.getResource("Backup").mkdir()
			self.getResource("Backup/dialogTemplate").mkdir()

		if self.getResource('Backup/config.json.template').exists():
			self.logInfo("Retreiving Backup Data")
			templateData = self.readTemplateData(self.getResource('config.json.template'))
			BackupTemplateData = self.readTemplateData(self.getResource('Backup/config.json.template'))

			# Check if config template file is not the same as the backup version
			if not templateData == BackupTemplateData:
				self.Commons.runSystemCommand(["rm", "-f", self.getResource('Backup/config.json.template')])
				self.Commons.runSystemCommand(["cp", self.getResource('config.json.template'), self.getResource('Backup/config.json.template')])
				self.addSlotValues()
		else:
			self.Commons.runSystemCommand(["cp", self.getResource('config.json.template'), self.getResource('Backup/config.json.template')])
			self.Commons.runSystemCommand(['cp', self.getResource(f'dialogTemplate/{self.activeLanguage()}.json'), self.getResource(f'Backup/dialogTemplate/{self.activeLanguage()}.json') ])
			self.logDebug(f"Just backed up your Radio configuration")

	def onBooted(self) -> bool:
		self.BackupPathRoutines()
		super().onBooted()
		return True

	def parsePlaylists(self, stationUrl):
		"""
		Parse .pls playlists and .m3u playlists and direct streaming links
		:param stationUrl: The selected URL to play
		:return:
		"""

		urlFormat = ""
		urlType = ""
		self.playlist = list()

		if "tuneIn" in stationUrl and ".pls" in stationUrl:
			urlFormat = "http.+(?=\r)"
			urlType = "tuneIn .pls"
		elif not "tuneIn" in stationUrl and ".pls" in stationUrl:
			urlFormat = "http.+"
			urlType = "General .pls"
		if ".m3u" in stationUrl and not ".m3u8" in stationUrl:
			urlFormat = "ht.+"
			urlType = "m3u"

		if not urlFormat:
			self._selectedStation = stationUrl
			return

		try:
			if self.getConfig(key='debugMode'):
				self.logInfo(f" {urlType} detected")
			req = urllib.request.urlopen(stationUrl)
			file = req.read()
			decodedFile = file.decode() # From bytes to str

			if self.getConfig(key='debugMode'):
				self.logDebug(f"Pre-parsed URL: {decodedFile}")
			pattern = re.compile(urlFormat)

			for item in pattern.findall(decodedFile):
				self.playlist.append(item)

		except Exception as msg:
			self.logWarning(f"{msg}")
