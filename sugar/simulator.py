import random

import gobject
import dbus

from sugar.presence import PresenceService
from sugar.graphics.iconcolor import IconColor
from sugar.p2p import Stream

_PRESENCE_SERVICE_TYPE = "_presence_olpc._tcp"

_nick_names = ['Aba', 'Abebe', 'Abebi', 'Abena', 'Abeni', 'Abeo', 'Abiba', 'Ada', 'Adah', 'Adana', 'Adanna', 'Adanya', 'Aissa', 'Akili', 'Alika', 'Ama', 'Amadi', 'Ameena', 'Ameenah', 'Ami', 'Amina', 'Aminah', 'Arziki', 'Asha', 'Ashia', 'Aziza', 'Baako', 'Binah', 'Binta', 'Bisa', 'Bolanle', 'Bunme', 'Caimile', 'Cataval', 'Chika', 'Chipo', 'Dalia', 'Dalila', 'Dayo', 'Deka', 'Delu', 'Denisha', 'Dore', 'Ebere', 'Fadhila', 'Faizah', 'Falala', 'Fayola', 'Feechi', 'Femi', 'Fisseha', 'Fola', 'Gamada', 'Ghalyela', 'Habika', 'Hada', 'Hadiya', 'Haiba', 'Halima', 'Hanzila', 'Hasina', 'Hija', 'Ilori', 'Iman', 'Imena', 'Iniko', 'Isabis', 'Isoke', 'Jahia', 'Jamelia', 'Jamila', 'Jamilah', 'Jamilia', 'Jamilla', 'Jamille', 'Jemila', 'Jendayi', 'Jina', 'Kabira', 'Kadija', 'Kafi', 'Kainda', 'Kali', 'Kalifa', 'Kanene', 'Kapera', 'Karimah', 'Kasinda', 'Keisha', 'Kesia', 'Lakeesha', 'Lateefah', 'Latrice', 'Latricia', 'Leal', 'Lehana', 'Limber', 'Lulu', 'Maha', 'Maizah', 'Malika', 'Mandisa', 'Mardea', 'Marjani', 'Marka', 'Nabelung', 'Nailah', 'Naima', 'Naja', 'Nakeisha', 'Narkeasha', 'Neda', 'Neema', 'Nichelle', 'Oba', 'Okoth', 'Ontibile', 'Orma', 'Pemba', 'Rabia', 'Rafiya', 'Ramla', 'Rashida', 'Raziya', 'Reta', 'Ridhaa', 'Saada', 'Sabra', 'Safara', 'Saidah', 'Salihah', 'Shasa', 'Shasmecka', 'Sibongile', 'Sika', 'Simbra', 'Sitembile', 'Siyanda', 'Sukutai', 'Tabita', 'Taifa', 'Taja', 'Takiyah', 'Tamala', 'Tamasha', 'Tanesha', 'Tanginika', 'Tanishia', 'Tapanga', 'Tarisai', 'Tayla', 'Tendai', 'Thandiwe', 'Tiesha', 'TinekaJawana', 'Tiombe', 'Wafa', 'Wangari', 'Waseme', 'Xhosa', 'Zabia', 'Zahara', 'Zahra', 'Zalika', 'Zanta', 'Zarina', 'Zina', 'Aba', 'Abebe', 'Abebi', 'Abena', 'Abeni', 'Abeo', 'Abiba', 'Ada', 'Adah', 'Adana', 'Adanna', 'Adanya', 'Aissa', 'Akili', 'Alika', 'Ama', 'Amadi', 'Ameena', 'Ameenah', 'Ami', 'Amina', 'Aminah', 'Amineh', 'Arziki', 'Asha', 'Ashia', 'Aziza', 'Baako', 'Binah', 'Binta', 'Bisa', 'Bolanle', 'Bunme', 'Caimile', 'Cataval', 'Chika', 'Chipo', 'Dalila', 'Dayo', 'Deka', 'Delu', 'Denisha', 'Dore', 'Ebere', 'Fadhila', 'Faizah', 'Falala', 'Fayola', 'Feechi', 'Femi', 'Fisseha', 'Fola', 'Gamada', 'Ghalyela', 'Habika', 'Hada', 'Hadiya', 'Haiba', 'Halima', 'Hanzila', 'Hasina', 'Hija', 'Ilori', 'Iman', 'Imena', 'Iniko', 'Isabis', 'Isoke', 'Jahia', 'Jamelia', 'Jamila', 'Jamilah', 'Jamilia', 'Jamilla', 'Jamille', 'Jemila', 'Jendayi', 'Jina', 'Kabira', 'Kadija', 'Kafi', 'Kainda', 'Kali', 'Kalifa', 'Kanene', 'Kapera', 'Karimah', 'Kasinda', 'Keisha', 'Kesia', 'Lakeesha', 'Lateefah', 'Latrice', 'Leal', 'Lehana', 'Limber', 'Lulu', 'Maha', 'Maizah', 'Malika', 'Mandisa', 'Mandisa', 'Mardea', 'Marjani', 'Marka', 'Nabelung', 'Nailah', 'Naima', 'Naja', 'Nakeisha', 'Narkeasha', 'Neda', 'Neema', 'Nichelle', 'Oba', 'Okoth', 'Ontibile', 'Orma', 'Pemba', 'Rabia', 'Rafiya', 'Ramla', 'Rashida', 'Raziya', 'Reta', 'Ridhaa', 'Saada', 'Sabra', 'Safara', 'Saidah', 'Salihah', 'Shasa', 'Shasmecka', 'Sibongile', 'Sika', 'Simbra', 'Sitembile', 'Siyanda', 'Sukutai', 'Tabita', 'Taifa', 'Taja', 'Takiyah', 'Tale', 'Tale green', 'Tamala', 'Tamasha', 'Tanesha', 'Tanginika', 'Tanishia', 'Tapanga', 'Tarisai', 'Tayla', 'Tendai', 'Thandiwe', 'Tiesha', 'TinekaJawana', 'Tiombe', 'Wafa', 'Wangari', 'Waseme', 'Xhosa', 'Zabia', 'Zahara', 'Zahra', 'Zalika', 'Zanta']

class _BotService(object):
	def __init__(self, bot):
		self._bot = bot

	def announce(self):
		props = { 'color':  self._bot.color.to_string() }
		pservice = PresenceService.get_instance()
		self._service = pservice.register_service(self._bot.name,
							_PRESENCE_SERVICE_TYPE, properties=props)

		self._stream = Stream.Stream.new_from_service(self._service)
		self._stream.register_reader_handler(
						self._handle_buddy_icon_request, "get_buddy_icon")
		self._stream.register_reader_handler(
						self._handle_invite, "invite")

	def _handle_buddy_icon_request(self):
		if self._bot.icon:
			fd = open(self._bot.icon, "r")
			icon_data = fd.read()
			fd.close()
			if icon_data:
				return base64.b64encode(self._icon)
		return ''

	def _handle_invite(self, issuer, bundle_id, activity_id):
		return ''

	def set_current_activity(self, activity_id):
		self._service.set_published_value('curact', dbus.String(activity_id))

class _ChangeActivityAction(object):
	def __init__(self, bot, activity_id):
		self._bot = bot
		self._activity_id = activity_id

	def execute(self):
		self._bot._service.set_current_activity(self._activity_id)

class _ShareChatAction(object):
	def __init__(self, bot, activity_id, title):
		self._bot = bot
		self._title = title
		self._id = activity_id 

	def execute(self):
		name = "%s [%s]" % (self._bot.name, self._id)
		stype = '_GroupChatActivity_Sugar_redhat_com._udp'
		properties = { 'title' : self._title,
					   'color' : self._bot.color.to_string() }
		address = u"232.%d.%d.%d" % (random.randint(0, 254),
									 random.randint(1, 254),
									 random.randint(1, 254))

		pservice = PresenceService.get_instance()
		pservice.register_service(name, stype, properties, address)

class _WaitAction(object):
	def __init__(self, bot, seconds):
		self._bot = bot
		self._seconds = seconds
	
	def execute(self):
		self._bot._pause_queue(self._seconds)

class Bot(object):
	def __init__(self):
		self.name = _nick_names[random.randint(0, len(_nick_names))]
		self.color = IconColor()
		self.icon = None

		self._queue = []

	def wait(self, seconds):
		action = _WaitAction(self, seconds)
		self._queue.append(action)

	def share_chat(self, activity_id, title):
		action = _ShareChatAction(self, activity_id, title)
		self._queue.append(action)

	def change_activity(self, activity_id):
		action = _ChangeActivityAction(self, activity_id)
		self._queue.append(action)

	def start(self):
		self._service = _BotService(self)
		self._service.announce()

		self._start_queue()

	def _idle_cb(self):
		self._next_action()
		return True

	def _pause_done_cb(self):
		self._start_queue()
		return False

	def _start_queue(self):
		self._queue_sid = gobject.idle_add(self._idle_cb)

	def _pause_queue(self, seconds):
		gobject.source_remove(self._queue_sid)
		gobject.timeout_add(int(seconds * 1000), self._pause_done_cb)

	def _next_action(self):
		if len(self._queue) > 0:
			action = self._queue.pop(0)
			action.execute()
