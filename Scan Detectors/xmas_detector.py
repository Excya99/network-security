from scapy.all import sniff

destinationPorts = set()
def processPacket(packet):
	#currentPacket = packet.summary()
	if packet["TCP"].flags == "FPU":
		destinationPorts.add(str(packet["TCP"].dport))
#capturing and processing first 1000 packets, monitoring loopback interface (for testing)
sniff(count=1000, filter="tcp", store=0, iface=["lo"], prn=processPacket)
for port in destinationPorts:
	print("Xmas Scan Detected on Port " + port)