import requests as r
import json
import hues
from clint.textui import prompt, puts, colored, validators, indent
from sys import argv

credentials = {}
conf_file = ''

def load_stuff(filename):
	global credentials
	global conf_file
	conf_file = filename
	with open(conf_file, 'r') as f:
		credentials = json.loads(f.read())

def save_session():
	global credentials
	global conf_file
	with open(conf_file, 'w+') as f:
		f.write(json.dumps(credentials))
	return "exit"

def get_messages():
    global credentials
    method = "https://api.vk.com/method/messages.get?access_token="
    resp = r.get(method + credentials["token"])
    return json.loads(resp.text)['response'][1:]

def display_unread():
	print(hues.huestr('    Unread Messages    ').white.bg_blue.bold.colorized)	
	mess = get_unread(get_messages())
	if not mess:
		 print(hues.huestr('    Nothing new, bro   ').white.bg_black.bold.colorized)
	for msg in mess:
		display_message(msg)
	# print('\n')
	return "displayed"

def display_all():
	print(hues.huestr('    All Messages    ').white.bg_blue.bold.colorized)	
	mess = get_messages()
	# if not mess:
	# 	 print(hues.huestr('    Nothing new, bro   ').white.bg_black.bold.colorized)
	prev = 0
	for i in range(len(mess)):
		prev = display_message(mess[i], not (mess[i]['uid']==mess[i-1]['uid']))
	return "displayed"


def display_message(message, pr_name=True):
	usr = get_username(message['uid'])

	if pr_name:
		print(hues.huestr(u' From {}:'.format(usr)).white.bold.colorized)
	with indent(3):
		puts(colored.white(message['body']))

def get_username(id):
    method = "https://api.vk.com/method/users.get?user_ids={0:d}".format(id)
    resp = r.get(method)
    usr = json.loads(resp.text)['response'][0]
    return u"{} {}".format(usr['first_name'], usr['last_name'])

def get_unread(msg_list):
    return [msg for msg in msg_list if msg['read_state'] == 0]

def send_message(uid, message):
    global token
    method = "https://api.vk.com/method/messages.send?access_token={token}&user_id={uid}&message={message}".format(token=token,uid=uid,message=message)
    resp = r.get(method)
    return json.loads(resp)

if __name__ == '__main__':

	load_stuff(argv[1])
	
	inst = "start"

	while inst != "exit":
	    options = [{'selector': '1','prompt':'see unread messages','return': display_unread},
	    		   {'selector': '2','prompt':'see all messages','return': display_all},
	    		   {'selector': '3','prompt':'send message','return': "send"},
	    		   {'selector': '4','prompt':'exit','return': save_session}]
	    
	    procedure = prompt.options("What next?", options)
	    
	    inst = procedure()

