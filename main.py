import subprocess
import re


def get_ip_and_netmask():
	# Execute ifconfig command
	result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE)
	output = result.stdout.decode()

	# Find the first non-loopback interface with an IP address
	inet_pattern = re.compile(r'inet (\d+\.\d+\.\d+\.\d+) netmask (0x[0-9a-fA-F]+)')
	for line in output.split('\n'):
		match = inet_pattern.search(line)
		if match and match.group(1) != '127.0.0.1':
			ip_address = match.group(1)
			netmask = match.group(2)
			return ip_address, netmask

	return None, None


def netmask_to_cidr(netmask):
	# Convert netmask from hex to dotted decimal
	netmask_hex = netmask[2:]
	netmask_bin = bin(int(netmask_hex, 16))[2:].zfill(32)
	cidr = str(netmask_bin.count('1'))
	return cidr


def main():
	ip_address, netmask = get_ip_and_netmask()
	if ip_address and netmask:
		cidr = netmask_to_cidr(netmask)
		print(f"{ip_address}/{cidr}")
	else:
		print("Unable to determine IP address and netmask")


if __name__ == "__main__":
	main()
