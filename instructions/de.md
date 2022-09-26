## Über den Skill

Dieser Skill ist ein einfaches Radio. Du kannst selber Sender hinzufügen oder entfernen. Schau dir dafür die Details weiter unten an!

Ein paar Sender sind voreingestellt, der Rest liegt an dir!

- TIP: Für eine mächtigeres Radio, versuche doch [Nepos MultiRoom Radio skill](https://github.com/poulsp/skill_MultiRoomRadioManager/blob/master/instructions/en.md)


## Füge deine eigenen Radiosender hinzu

Suche zunächst die URL zu deinem Radiosender heraus. Weiter gehts wenn du die URL hast ...

1. Öffne config.json.template im skills Verzeichnis
2. Füge die URL in der "values" Liste in der folgenden Form ein

*Beispiel Format...*


"values": {
			"Sprechbarer Name des Senders": "URL zum Stream"
			}

	
*Beispiel:*


"values": {
			"Jazz": "http://theJazzStationURL.pls",
			"eighties Music": "http://80sMusicUrl.m3u",
			"B B C": "http://bbcwssc.ic.llnwd.net/stream/bbcwssc_mp1_ws-eieuk"
			}

			
### Die URL kann in den folgenden Formaten sein:


- *.pls URLS
- *.m3u URLS
- Direkte stream Links

NOTE :  *.m3u8 URLS sind derzeit nicht unterstützt

## Funktionen des Skills

Zum Spielen des Radios

* Frage Alice:
- Spiele den B B C Radiosender 
- Spiele Radiosender Nummer 3

* Oder wähle den Sender in den Einstellungen:
- Wähle den Sender im Drop-Down: Dieser wird gleich automatisch gespielt
- Schalte "turn on the radio" in den Einstellungen an und mit dem Speichern läuft das Radio los!

Zwischen den Sendern kannst du so wechseln:

1. sage -> Spiele den <Neuer Sender> Radiosender!
2. Wähle es in den Skilleinstellungen im Drop-Down aus
3. sage -> Spiele Radiosender Nummer <Nummer des neuen Senders>.

NOTE: Der Skill redet meist von Radio und Radiosendern um Kollissionen mit Fernseher, Spotify und ähnlichem zu vermeiden!

## Stoppe das Radio
Abhängig von der Wiedergabelautstärke kann es sein, dass dich Alice nicht hört oder versteht.
Ansonsten sag einfach "Schalte das Radio aus"!


Alternativ hast du folgende Möglichkeiten:

1. Schreibe in Alices DialogView "Schalte das Radio aus"
2. Öffne die Skill-Einstellungen und wähle die Option "stop the radio".
3. Schreibe "mpc stop" in der Kommandozeile
