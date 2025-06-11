import os
if __name__ == "__main__":
	if os.geteuid() != 0:
		print("This script must be run with sudo or as the root user.")
		exit()
	SERVICE_FILE_PATH = "/usr/lib/systemd/system/clipboardstealer.service"
	try:
		os.system("systemctl stop clipboardstealer.service")
		os.system("systemctl disable clipboardstealer.service")
		os.remove(SERVICE_FILE_PATH)
		print("Clipboard stealer has successfully been removed. Manually remove the stealer python file and the log file.")
	except Exception as e:
		print("This script could not remove clipboard stealer.")
