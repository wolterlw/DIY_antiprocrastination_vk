from clint.textui import prompt, puts, colored, validators, indent
from sys import argv
from vk_api import Session,Message
import hues


def apply_session(sess):
	def decorator(func):
		def wrapper(*args,**kwargs):
			return func(sess,*args,**kwargs)
		return wrapper
	return decorator

sess = Session(argv[1])

@apply_session(sess)
def display_unread(sess):
	print(hues.huestr('    Unread Messages    ').white.bg_blue.bold.colorized)	
	mess = sess.get_unread(sess.get_messages())
	if not mess:
		 print(hues.huestr('    Nothing new, bro   ').white.bg_black.bold.colorized)
	for msg in mess:
		display_message(msg)
	# print('\n')
	return "displayed"

@apply_session(sess)
def display_all(sess):
	print(hues.huestr('    All Messages    ').white.bg_blue.bold.colorized)	
	mess = sess.get_messages()
	for i in range(len(mess)):
		display_message(mess[i], not (mess[i].from_id ==mess[i-1].from_id))
	return "displayed"

@apply_session(sess)
def display_message(sess,message, pr_name=True):
	usr = sess.get_username(message.from_id)

	if pr_name:
		print(hues.huestr(u' From {}:'.format(usr)).white.bold.colorized)
	with indent(3):
		puts(colored.white(message.body))
	with indent(5):
		for p in message.photos:
			puts(colored.white(p))
		# for f in message.fwd: 
		# 	print f.__repr__()

@apply_session(sess)
def send_message(sess):
	friends = sess.get_friends()

	options = [{'selector': i, 'prompt': friends[j],'return': j}
				for i,j in enumerate(friends.keys())]

	uid = prompt.options("select friend:",options)
	message = prompt.query("text: ")
	sess.send_message(uid,message)


if __name__ == '__main__':

	#add path to your local file of configuration which stores {"token": "<your access token>"}
	
	inst = "start"
	options = [{'selector': '1','prompt':'see unread messages','return': display_unread},
	    		   {'selector': '2','prompt':'see all messages','return': display_all},
	    		   {'selector': '3','prompt':'send message','return': send_message},
	    		   {'selector': '4','prompt':'exit','return': sess.close}]
	    
	while inst != "exit":
	    procedure = prompt.options("What next?", options)
	    
	    inst = procedure()

