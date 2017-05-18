#Clipboard_monitor
#A module to monitor for clipboard changes
#By: Damien Lindley
#Created: 20th April 2017
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from win32clipboard import *
from logHandler import log

class clipboard_monitor(object):
	def __init__(self):
		log.debug("Initialising clipboard monitor.")
		self.get_clipboard()

	def get_clipboard(self):
		log.debug("Enumerating clipboard data...")
		__clipboard_data=self.enumerate_clipboard()

	def enumerate_clipboard(self):
		data={}
		log.debug("Opening the clipboard for enumeration.")
		try:
			OpenClipboard(None)
		except:
			log.debug("Clipboard failed to open. Cannot enumerate.")
			return data
		format=0
		while True:
			try:
				format=EnumClipboardFormats(format)
				log.debug("Retrieving clipboard format: %d"%format)
				if format==0: break
				pos=str(format)
				log.debug("Retrieving data for format %s"%pos)
				data[pos]=GetClipboardData(format)
				log.debug("Data retrieved: %r"%data[pos])
			except:
				log.debug("Cannot retrieve data.")
				break
		log.debug("Closing clipboard.")
		CloseClipboard()
		return data

	def valid_data(self):
		log.debug("Validating clipboard data.")
		comparison=self.enumerate_clipboard()
		if comparison=={}:
			log.debug("No data appears to be on the clipboard.")
			return False

		log.debug("The clipboard contains valid data.")
		return True

	def changed(self):
		log.debug("Checking for clipboard changes.")
		comparison=self.enumerate_clipboard()
		if comparison==self.__clipboard_data:
			log.debug("No changes detected.")
			return False

		log.debug("Clipboard data has changed. Updating cached data...")
		self.__clipboard_data=comparison
		return True

	__clipboard_data={}
