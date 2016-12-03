import vk_api
import subprocess
from sys import argv
from time import sleep

sess = vk_api.Session(argv[1])
#in argv[1] you should pass the path to your configurations file

def get_unread(sess,last_date=-1):
	mess = sess.get_unread(sess.get_messages())

	new = [ msg for msg in mess if (msg['date'] > last_date) ]
	if new:
		last_date = max(new, key=lambda x: x['date'])['date']
	return (new,last_date)

if __name__ == '__main__':
	unread,last_date = get_unread(sess)

	while True:
		sleep(10)
		new,last_date = get_unread(sess, last_date)
		for msg in new:
			stuff = (sess.get_username(msg['uid']), msg['body'])
					 #path - path to the icon you want to display
			subprocess.Popen(
				["notify-send", 
				 u"{0}: {1}".format(*stuff)]
				)