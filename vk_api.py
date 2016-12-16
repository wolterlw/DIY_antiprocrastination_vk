import requests as r
import json

class Session(object):
	def __init__(self, path):
		self._conf_file = path
		with open(self._conf_file, 'r') as f:
			self._credentials = json.loads(f.read())
		if not 'friends' in self._credentials:
		    self._credentials['friends'] = {}

	def close(self):
		with open(self._conf_file, 'w+') as f:
			f.write(json.dumps(self._credentials))
		return "exit"
	
	def get_messages(self):
	    method = "https://api.vk.com/method/messages.get?access_token="
	    resp = r.get(method + self._credentials["token"])
	    return [Message(msg) for msg in json.loads(resp.text)['response'][1:]]

	def get_username(self,id):
		if id in self._credentials['friends']:
			return self._credentials['friends'][id]

		else:
		    method = "https://api.vk.com/method/users.get?user_ids={0:d}".format(id)
		    resp = r.get(method)
		    usr = json.loads(resp.text)['response'][0]
		    name = u"{} {}".format(usr['first_name'], usr['last_name'])
		    
		    self._credentials['friends'][id] = name
		    return name

	def get_friends(self):
		if self._credentials['friends'] == {}:
			mess = self.get_messages()
			for m in mess:
				self._credentials[m.from_id] = self.get_username(m.from_id)

		return self._credentials['friends']

	def get_unread(self,msg_list):
	    return [msg for msg in msg_list if msg.read_state == 0]

	def send_message(self,uid, message):
	    method = "https://api.vk.com/method/messages.send?access_token={token}&user_id={uid}&message={message}".format(
	    	token=self._credentials["token"],uid=uid,message=message)
	    resp = r.get(method)
	    # return json.loads(resp)['response'][1:]

	def get_dialogs(self,num=10):
	    method = "https://api.vk.com/method/messages.getDialogs?access_token={}&count={}".format(
	    		  self._credentials["token"],num_messages)
	    resp = r.get(method)
	    return json.loads(resp.text)['response'][1:]

	def get_mess_from_user(self,uid,num=10):
		method = "https://api.vk.com/method/messages.getHistory?access_token={token}&peer_id={uid}&count={num}&rev=0".format(
				  token=self._credentials["token"],uid=uid,num=num)
		resp = r.get(method)
		return resp['response']['items']


class Message():
	def __init__(self,msg):
		self.from_id = msg['uid']
		self.body = msg['body']
		self.photos = []
		self.fwd = []
		if 'read_state' in msg.keys():
			self.read_state = msg['read_state']
		else:
			self.read_state = 1

		if "attachments" in msg.keys():
			self.photos = [att['photo']['src_xxbig'] 
						   for att in msg['attachments'] if att['type'] == 'photo']

		if "fwd_messages" in msg.keys():
			self.fwd = [Message(fwd) for fwd in msg["fwd_messages"]]

	def __repr__(self):
		return u"{from_}: {text}\n\tfwd = {fwd}\n\tattachments = {att}".format(
				from_=self.from_id, text = self.body, fwd = self.fwd, att = self.photos)

	def __str__(self):
		return self.__repr__()

class Dialogue():
	def __init__(self,uid,session):
		self._session = session
		self._other = uid
		self.other_name = session.get_username(uid)
	
	def send_message(self,message):
		self._session.send_message(self._uid,message)

	# def get_messages(self):