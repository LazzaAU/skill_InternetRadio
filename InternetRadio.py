import json

from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class InternetRadio(AliceSkill):
	"""
	Author: lazzaAU
	Description: Listen to internet radio stations
	"""


	def __init__(self):

		self._templatePath = '/InternetRadio/config.json.template'
		self._selectedStation = ""
		self._data = dict()

		super().__init__()


	@IntentHandler("ListenToRadio")
	def setupTheStation(self, session: DialogSession, **_kwargs):
		# Read the config.json.template file to get the list of values
		self._data = self.readTemplateData()

		# If user has not specified a station, just play the default station
		if not 'RadioStation' in session.slotsAsObjects and not 'number' in session.slotsAsObjects:
			self.playExistingStation(session=session)
			return

		# If user specified the station, match it up to the url
		# if user specified a number, select that line from the list if available
		if session.slotValue('number'):
			listLength = len(self._data)
			number: int = session.slotValue('number')

			# if user asks for list number that doesn't exist
			if number > listLength:
				self.logWarning('Number requested was larger than list... aborting')
				self.endDialog(
					text='Provided number was out of range. Ask me again correctly'
				)
				return
			else:
				counter = 1
				for item in self._data:
					# update the config with selected url via number selection
					if counter == number:
						if self._data.get(item) == self.getConfig('radioStations'):
							return self.playExistingStation(session)

						self._selectedStation = self._data.get(item)
						self.updateConfig(key='radioStations', value=self._selectedStation)
						return self.playExistingStation(session)
					counter += 1

		choosenStation = session.slotValue('RadioStation')

		for key in self._data:
			# update the config with choosen station via station name
			if key in choosenStation:
				# If station being requested is existing station, just play it
				if self._data.get(key) == self.getConfig('radioStations'):
					return self.playExistingStation(session)

				self._selectedStation = self._data.get(key)
				self.updateConfig(key='radioStations', value=self._selectedStation)
				return self.playExistingStation(session)
			else:
				self.endDialog(
					text='Couldn\'t find that station. Please try again'
				)


	def configUpdated(self, dt) -> bool:
		self.logInfo(f'Updated slot Values in dialogTemplate')
		self._data = self.readTemplateData()
		self.addSlotValues()
		return True


	# Read and store the template list
	def readTemplateData(self):
		configPath = self.getResource('config.json.template')
		data = json.loads(configPath.read_text())
		tempData = dict()

		# Trim the original json to just the relevant values
		for key in data['radioStations']['values']:
			tempData[key] = data['radioStations']['values'][key]

		return tempData


	def playExistingStation(self, session):
		if not self._selectedStation:
			self._selectedStation = self.getConfig('radioStations')
		self.logInfo(f'Now be playing radio station from "{self._selectedStation}"')
		self.Commons.runSystemCommand(f'mpc clear '.split())
		self.Commons.runSystemCommand(f'mpc add {self._selectedStation}'.split())
		self.Commons.runSystemCommand(f'mpc play'.split())
		self._selectedStation = ""
		self.endDialog(
			sessionId=session.sessionId,
			text='ok'
		)


	def addSlotValues(self) -> bool:

		file = self.getResource(f'dialogTemplate/{self.activeLanguage()}.json')
		if not file:
			return False
		# load the dialogTemplate file data
		data = json.loads(file.read_text())

		slotValue = list()
		# Setup the slot values
		for item in self._data:
			tempData = {'value': item, 'synonyms': []}
			slotValue.append(tempData)

		# Add slot values to the dialogTemplate slotType
		for i, suggestedSlot in enumerate(data['slotTypes']):
			if "radiostation" in suggestedSlot['name'].lower():
				data['slotTypes'][i]['values'] = slotValue

		file.write_text(json.dumps(data, ensure_ascii=False, indent=4))

		return True
