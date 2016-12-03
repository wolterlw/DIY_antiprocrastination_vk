from clint.textui import prompt, puts, colored, validators, indent
from sys import argv
from vk_api import Session
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
	# if not mess:
	# 	 print(hues.huestr('    Nothing new, bro   ').white.bg_black.bold.colorized)
	prev = 0
	for i in range(len(mess)):
		prev = display_message(mess[i], not (mess[i]['uid']==mess[i-1]['uid']))
	return "displayed"

@apply_session(sess)
def display_message(sess,message, pr_name=True):
	usr = sess.get_username(message['uid'])

	if pr_name:
		print(hues.huestr(u' From {}:'.format(usr)).white.bold.colorized)
	with indent(3):
		puts(colored.white(message['body']))

if __name__ == '__main__':
	inst = "start"

	while inst != "exit":
	    options = [{'selector': '1','prompt':'see unread messages','return': display_unread},
	    		   {'selector': '2','prompt':'see all messages','return': display_all},
	    		   {'selector': '3','prompt':'send message','return': "send"},
	    		   {'selector': '4','prompt':'exit','return': sess.close}]
	    
	    procedure = prompt.options("What next?", options)
	    
	    inst = procedure()

