#!/usr/bin/env python
import sys, getopt
import urllib2, base64, uuid
import json
# wol + SSDP
import socket


###########################################################
#
#	GLOBAL VAR & DEFINITIONS
#
###########################################################
SONYIP = "192.168.1.72"
#CLIENTID = "bunk3r:"+str(uuid.uuid4())
#CLIENTID = "bunk3r:a484c257-c10e-46b8-8ab2-411dcdcbdeea"
#NICKNAME = "bunk3r (braviapy)"
CLIENTID = 'TVSideView:eb1214c4-321d-47ab-948d-9b9ebb36354e'
NICKNAME = 'Nexus 7 (TV SideView)'


# B0:10:41:72:C6:83
macaddr = "B0:10:41:72:C6:83"

_AUTHORIZATION = json.dumps(
{	"method":"actRegister",
	"params":[
	{
		"clientid":CLIENTID,
		"nickname":NICKNAME,
		"level":"private"},[
		{
			"value":"yes",
			"function":"WOL"}
		]
	],
	"id":1,
	"version":"1.0"}
)


###########################################################
#
#	Usage
#
###########################################################
def usage ():
	print("Usage: %s (-h|--help) (-p|--pin <pin>) (-v|--verbose) (-d|--discover) (-w|--wol <macaddr>) (-r|--remote)" % sys.argv[0])

	

###########################################################
#
#	Build JSON commands
#
###########################################################
def jdata_build(method, params):
	if params:
		ret =  json.dumps({"method":method,"params":[params],"id":1,"version":"1.0"})
	else:
		ret =  json.dumps({"method":method,"params":[],"id":1,"version":"1.0"})
	return ret

	

###########################################################
#
#	Remote Control
#
###########################################################
def remote_control(cookie, verbose = False):
	# get Remote IRCC commands
	print "[*] getRemoteControllerInfo"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getRemoteControllerInfo", ""), cookie);
	data = resp['result'][1]
	commands = {}
	for item in data:
		if verbose:
			print item['value'], item['name']
		commands[item['name']] = item['value']

	print "[p] PowerOff:", commands['PowerOff']
	print "[V] VolumeUp:", commands['VolumeUp']
	print "[v] VolumeDown", commands['VolumeDown']
	print "[C] ChannelUp", commands['ChannelUp']
	print "[c] ChannelDown", commands['ChannelDown']
	for num in range(0,10):
			if commands['Num'+str(num)]:
				print "["+str(num)+"] Num"+str(num)+":", commands['Num'+str(num)]
	while True:
		num = raw_input()
		if num == '0':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '1':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '2':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '3':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '4':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '5':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '6':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '7':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '8':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);
		elif num == '9':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['Num'+str(num)], cookie);	
		elif num == 'p':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['PowerOff'], cookie);
		elif num == 'V':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['VolumeUp'], cookie);
		elif num == 'v':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['VolumeDown'], cookie);
		elif num == 'C':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['ChannelUp'], cookie);
		elif num == 'c':
			resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", commands['ChannelDown'], cookie);	
		else:
			print "Remote Controller: exit!"
			break
	return None
	
	

###########################################################
#
#	WAKE ON LAN
#
###########################################################
def wakeonlan(ethernet_address):
	import struct
	addr_byte = ethernet_address.split(':')
	hw_addr = struct.pack('BBBBBB', int(addr_byte[0], 16),
	int(addr_byte[1], 16),
	int(addr_byte[2], 16),
	int(addr_byte[3], 16),
	int(addr_byte[4], 16),
	int(addr_byte[5], 16))
	msg = b'\xff' * 6 + hw_addr * 16
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(msg, ('<broadcast>', 9))
	s.close()



###########################################################
#
#	DISCOVER IP VIA SSDP PROTOCOL (UDP 1900 PORT)
#
###########################################################
def DISCOVER_via_SSDP ():
	import select, re
	SSDP_ADDR = "239.255.255.250";
	SSDP_PORT = 1900;
	SSDP_MX = 1;
	SSDP_ST = "urn:schemas-sony-com:service:ScalarWebAPI:1";

	ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
		"HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT) + \
		"MAN: \"ssdp:discover\"\r\n" + \
		"MX: %d\r\n" % (SSDP_MX, ) + \
		"ST: %s\r\n" % (SSDP_ST, ) + "\r\n";

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#select.select([sock], [], [], 10)
	sock.settimeout(5.0)
	dest = socket.gethostbyname(SSDP_ADDR)
	sock.sendto(ssdpRequest, (dest, SSDP_PORT))
	sock.settimeout(5.0)
	try: 
		data = sock.recv(1000)
	except socket.timeout:
		print "No Bravia found (timed out)!"
		sys.exit(1)
	response = data.decode('utf-8')
	match = re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", response)
	if match:                      
		return match.group()
	else:
		return SONYIP



###########################################################
#
#	GET COOKIE FROM SONY BRAVIA TV via HTTP
#		- if pin passed sends Basic Authentication
#		- otherwise tries to get cookie
#
###########################################################
def bravia_auth ( ip, port, url, params, pin ):
	req = urllib2.Request('http://'+ip+':'+port+'/'+url, params)
	cookie = None
	response = None
	
	if pin:
		username = ''
		base64string = base64.encodestring('%s:%s' % (username, pin)).replace('\n', '')
		req.add_header("Authorization", "Basic %s" % base64string)
		req.add_header("Connection", "keep-alive")
		
	try:
		response = urllib2.urlopen(req)
		
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		return None
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		return None
    	#sys.exit(1)
		
	else: 
		for h in response.info().headers:
			if h.find("Set-Cookie") > -1:
				cookie=h			
		if cookie:
			cookie = response.headers['Set-Cookie']
			return cookie
		#html = response.info().items(),response.read()
		#print "[i] Response:", html
		return None
		

###########################################################
#
#	SEND JSON REQUEST via HTTP (cookie required)
#
###########################################################
def bravia_req_json( ip, port, url, params, cookie ):
	req = urllib2.Request('http://'+ip+':'+port+'/'+url, params)
	req.add_header('Cookie', cookie)
	try:
		response = urllib2.urlopen(req)
		
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		#sys.exit(1)

	else:
		#json 2 dictionary
		html = json.load(response)
		#print "[i] Response:", html
		return html

	
	
	
###########################################################
#
#	SEND IRCC REQUEST via HTTP (cookie required)
#
###########################################################
def bravia_req_ircc( ip, port, url, params, cookie ):
	req = urllib2.Request('http://'+ip+':'+port+'/'+url, "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>"+params+"</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>")
	req.add_header('SOAPACTION', 'urn:schemas-sony-com:service:IRCC:1#X_SendIRCC')
	req.add_header('Cookie', cookie)
	
	try:
		response = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "[W] HTTPError: " + str(e.code)
		
	except urllib2.URLError, e:
		print "[W] URLError: " + str(e.reason)
		#sys.exit(1)
	else:
		tree = response.read()
		return tree


	
	
	
###########################################################
#
#	[MAIN]
#
###########################################################
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:vdw:r", ["help", "pin=", "verbose", "discover", "wol=", "remote"])

	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)

	output = None
	verbose = False
	remote = False
	wol = False
	
	pin = "0000"
	
	for o, a in opts:
		if o == "-v":
			verbose = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		elif o in ("-p", "--pin"):
			pin = a
		elif o in ("-d", "--discover"):
			found = DISCOVER_via_SSDP()
			if found:
				print "Bravia found on", found
			else:
				print "Bravia NOT found!"
			sys.exit()
		elif o in ("-w", "--wol"):
			#macaddr = a
			wol = True
		elif o in ("-r", "--remote"):
			remote = True
		else:
			assert False, "unhandled option"

	if wol:
		wakeonlan(macaddr)
		sys.exit()

	# first request (AUTH 1)	
	print "[*] AccessControl"
	cookie = bravia_auth(SONYIP, "80", "sony/accessControl", _AUTHORIZATION, None );
	# send PIN if not cookie
	if not cookie:
		print "Sending PIN ", str(pin)
		cookie = bravia_auth(SONYIP, "80", "sony/accessControl", _AUTHORIZATION, pin );
		# exit if not cookie again (NO AUTH)
		if not cookie:
			print "Pairing failed!"
			sys.exit(0)
	else:
		print "Registered!"
		print "CLIENTID=%s" % (CLIENTID)
		print "NICKNAME=%s" % (NICKNAME)
		if verbose:
			print "Cookie:", cookie

	if remote:
		remote_control(cookie, verbose);
		sys.exit()
	

	print "[*] getPlayingContent"
	resp = bravia_req_json(SONYIP, "80", "sony/avContent", jdata_build("getPlayingContentInfo", None), cookie);
	#print json.dumps(resp.get('result'), indent=4)
	data = resp['result']
	for item in data:
		print "Program Title:", item["programTitle"]
		print "Title:", item["title"]
		print "MediaType:", item["programMediaType"]
	if verbose:
		print "RESULT: ", json.dumps(data), "\n"

	print "[*] getSystemInformation"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getSystemInformation", None), cookie);
	if not resp.get('error'):
		print json.dumps(resp.get('result'), indent=4)
	else:
		print "JSON request error", json.dumps(resp, indent=4)
	
	print "[*] getNetworkSettings"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getNetworkSettings", None), cookie);
	if not resp.get('error'):
		print json.dumps(resp.get('result'), indent=4)
	else:
		print "JSON request error", json.dumps(resp, indent=4)

	print "[*] getMethodTypes"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getMethodTypes", "1.0"), cookie);
	if not resp.get('error'):
		# __ results __ NOT __ result __
		print json.dumps(resp.get('results'), indent=4)
	else:
		print "JSON request error", json.dumps(resp, indent=4)

	print "[*] getWolMode"
	resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_build("getWolMode", None), cookie);
	if not resp.get('error'):
		print json.dumps(resp.get('result'), indent=4)
	else:
		print "JSON request error", json.dumps(resp, indent=4)


if __name__ == "__main__":
	main()

	
	
###########################################################
#
#	END - OLD & TRASH
#
###########################################################
#jdata_auth = json.dumps({"id":1,"method":"actRegister","version":"1.0","params":[{"clientid":CLIENTID,"nickname":NICKNAME},[{"clientid":CLIENTID,"value":"yes","nickname":NICKNAME,"function":"WOL"}]]})
# pin passed
#if len(sys.argv) == 2:
#	pin = str(sys.argv[1])
	#jdata_req = json.dumps({"method":"getMethodTypes","params":["1.0"],"id":1,"version":"1.0"})
	#resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_req, cookie);
	#print "\n[*] getMethodTypes\n-----------------------------------\n", json.dumps(resp, indent=4)


	# exit via IRCC
	#ircc_req = "AAAAAQAAAAEAAABjAw=="
	#print "[*] Sending IRCC command:", ircc_req
	#resp = bravia_req_ircc(SONYIP, "80", "sony/IRCC", ircc_req, cookie);
	#print resp


	#jdata_req = json.dumps({"method":"getWolMode","params":[],"id":1,"version":"1.0"})
	#print "-----------------------------------"
	#print "[*] getWolMode"
	#resp = bravia_req_json(SONYIP, "80", "sony/system", jdata_req, cookie);
	#print json.dumps(resp.get('result'), indent=4)

