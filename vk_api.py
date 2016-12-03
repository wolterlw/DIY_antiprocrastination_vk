import requests as r
import json

class Session(object):
	def __init__(self, path):
		self._conf_file = path
		with open(self._conf_file, 'r') as f:
			self._credentials = json.loads(f.read())

	def close(self):
		with open(self._conf_file, 'w+') as f:
			f.write(json.dumps(self._credentials))
		return "exit"
	
	def get_messages(self):
	    method = "https://api.vk.com/method/messages.get?access_token="
	    resp = r.get(method + self._credentials["token"])
	    return json.loads(resp.text)['response'][1:]

	def get_username(self,id):
	    method = "https://api.vk.com/method/users.get?user_ids={0:d}".format(id)
	    resp = r.get(method)
	    usr = json.loads(resp.text)['response'][0]
	    return u"{} {}".format(usr['first_name'], usr['last_name'])

	def get_unread(self,msg_list):
	    return [msg for msg in msg_list if msg['read_state'] == 0]

	def send_message(self,uid, message):
	    method = "https://api.vk.com/method/messages.send?access_token={token}&user_id={uid}&message={message}".format(
	    	token=self._credentials["token"],uid=uid,message=message)
	    resp = r.get(method)
	    return json.loads(resp)