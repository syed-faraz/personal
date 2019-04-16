#SNMP Firewall Strings

import paramiko
import telnetlib
import getpass
import time
import colorama
import numpy as np
from colorama import init
init(autoreset = True)
from colorama import Fore

print
print
print(Fore.GREEN+ "*****************************")
print
print(Fore.GREEN+ "     Welcome to AutoNet    \n")
print
print(Fore.GREEN+ "*****************************")
print
print

def login():
	try:
		login.username = raw_input("\nEnter your username:\n")
		login.password = getpass.getpass("\nEnter your password:\n")
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect("39.251.0.106", port=22, username=login.username, password=login.password, look_for_keys=False, allow_agent=False)
		ssh_channel = ssh.invoke_shell()
		output = ssh_channel.recv(65535)
		ssh.close()
	except:
		print (Fore.RED + '***Authentication failed, please try again***\n')
		login()
login()
	
def SD_Network():
	
	SD_Network.devicenames = []
	SD_Network.deviceIPs = []
	completed = []
	not_found = []
	no_login = []
	standby = []

	with open("firenew.txt") as f: 			
		for line in f: 			
			line1 = line.lower()
			device,address = line1.split(',')
			dev = device.replace('-','')
			d = dev.replace('_','')
			add = address.replace('\xa0','')
			ip = add.replace('\n','')					
			if 'fw' in d:
				SD_Network.devicenames.append(d)
				SD_Network.deviceIPs.append(ip)			
				
	for j in range (0,len(SD_Network.devicenames)):						
		print (Fore.GREEN + "\nLogging into "+ str(SD_Network.devicenames[j])+ "("+ str(SD_Network.deviceIPs[j])+")""....\n")							
		try:	
			HOST = SD_Network.deviceIPs[j]
									
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(HOST, port=22, username=login.username, password=login.password, look_for_keys=False, allow_agent=False)

			ssh_channel = ssh.invoke_shell()
			output = ssh_channel.recv(65535)

			ssh_channel.send("enable\n")
			time.sleep(.5)
			output = ssh_channel.recv(65535)
												
			ssh_channel.send(login.password + '\n')
			time.sleep(.5)
			output = ssh_channel.recv(65535)
			
			ssh_channel.send("\nterminal length 0\n")
			time.sleep(1)		
			output = ssh_channel.recv(65535)
			
			ssh_channel.send("\nsh failover | in This\n")
			time.sleep(1)		
			output = ssh_channel.recv(65535)
				
			if 'Standby' in output:
				print(Fore.RED+"\nThis is the standby firewall, logging out and logging into the next one...\n")
				standby.append(SD_Network.devicenames[j])
					
			if 'Active' in output:
				print(Fore.GREEN+"\nThis is the Active firewall\n")
					
				ssh_channel.send("\nmore system:running-config | i snmp-server host outside 159.140.176.17\n")
				time.sleep(5)
				
				output1 = ssh_channel.recv(65535)

				ssh_channel.send("\nmore system:running-config | i snmp-server host inside 159.140.176.17\n")
				time.sleep(5)
				
				output2 = ssh_channel.recv(65535)				
				
				if "snmp-server host outside 159.140.176.17 poll community 7rAq@+ef" in output1:
					line = output1.split('\n')							
					lines = line[2:-1]
														
					print("\n----------work plan---------\n")
					print("\nconf t\n")
					for x in lines:
						y = x.replace('\r','')
						print("no " +y)
					print("\nsnmp-server host outside 159.140.177.127 community 7rAq@+ef\n")
					print("exit\n")
					print("wr mem\n")
					
					ssh_channel.send("\nconf t\n")
					time.sleep(.5)
					for x in lines:
						y = x.replace('\r','')
						ssh_channel.send("no " +y)
						time.sleep(.5)
					ssh_channel.send("\nsnmp-server host outside 159.140.177.127 community 7rAq@+ef\n")
					time.sleep(.5)
					ssh_channel.send("exit\n")
					time.sleep(.5)
					ssh_channel.send("wr mem\n")
					time.sleep(10)
					ssh_channel.send("exit\n")
					output = ssh_channel.recv(65535)
					
					print output
					
					completed.append(SD_Network.devicenames[j])
					a1 = open ("SNMP.txt","a")
					a1.write(output)
					
				if "snmp-server host inside 159.140.176.17 poll community 7rAq@+ef" in output2:
					line = output2.split('\n')							
					lines = line[2:-1]
														
					print("\n----------work plan---------\n")
					print("\nconf t\n")
					for x in lines:
						y = x.replace('\r','')
						print("no " +y)
					print("\nsnmp-server host inside 159.140.177.127 community 7rAq@+ef\n")
					print("exit\n")
					print("wr mem\n")
					
					ssh_channel.send("\nconf t\n")
					time.sleep(.5)
					for x in lines:
						y = x.replace('\r','')
						ssh_channel.send("no " +y)
						time.sleep(.5)
					ssh_channel.send("\nsnmp-server host inside 159.140.177.127 community 7rAq@+ef\n")
					time.sleep(.5)
					ssh_channel.send("exit\n")
					time.sleep(.5)
					ssh_channel.send("wr mem\n")
					time.sleep(10)
					ssh_channel.send("exit\n")
					output = ssh_channel.recv(65535)
					
					print output
					
					completed.append(SD_Network.devicenames[j])
					a1 = open ("SNMP.txt","a")
					a1.write(output)
					
				if "snmp-server host outside 159.140.176.17 poll community 7rAq@+ef" not in output1 and "snmp-server host inside 159.140.176.17 poll community 7rAq@+ef" not in output2:
					print(Fore.RED + "\nThe string not found\n")
					not_found.append(SD_Network.devicenames[j])
			
			else: 
				ssh_channel.send("\nsh failover\n")
				time.sleep(3)		
				output2 = ssh_channel.recv(65535)
				
				if 'Failover Off' in output2:
			
					print(Fore.RED+"\nFailover is off. This is a standalone firewall\n")
						
					ssh_channel.send("\nmore system:running-config | i snmp-server host outside 159.140.176.17\n")
					time.sleep(5)
					
					output3 = ssh_channel.recv(65535)
					
					ssh_channel.send("\nmore system:running-config | i snmp-server host inside 159.140.176.17\n")
					time.sleep(5)
					
					output4 = ssh_channel.recv(65535)					
					
					if "snmp-server host outside 159.140.176.17 poll community 7rAq@+ef" in output3:
						line = output3.split('\n')
								
						lines = line[2:-1]
															
						print("\n----------work plan---------\n")
						print("\nconf t\n")
						for x in lines:
							y = x.replace('\r','')
							print("no " +y)
						print("\nsnmp-server host outside 159.140.177.127 community 7rAq@+ef\n")
						print("exit\n")
						print("wr mem\n")
						
						ssh_channel.send("\nconf t\n")
						time.sleep(.5)
						for x in lines:
							y = x.replace('\r','')
							ssh_channel.send("no " +y)
							time.sleep(.5)
						ssh_channel.send("\nsnmp-server host outside 159.140.177.127 community 7rAq@+ef\n")
						time.sleep(.5)
						ssh_channel.send("exit\n")
						time.sleep(.5)
						ssh_channel.send("wr mem\n")
						time.sleep(10)
						ssh_channel.send("exit\n")
						output = ssh_channel.recv(65535)
						
						print output
						
						completed.append(SD_Network.devicenames[j])
						a1 = open ("SNMP.txt","a")
						a1.write(output)
						
					if "snmp-server host inside 159.140.176.17 poll community 7rAq@+ef" in output4:
						line = output4.split('\n')
								
						lines = line[2:-1]
															
						print("\n----------work plan---------\n")
						print("\nconf t\n")
						for x in lines:
							y = x.replace('\r','')
							print("no " +y)
						print("\nsnmp-server host inside 159.140.177.127 community 7rAq@+ef\n")
						print("exit\n")
						print("wr mem\n")
						
						ssh_channel.send("\nconf t\n")
						time.sleep(.5)
						for x in lines:
							y = x.replace('\r','')
							ssh_channel.send("no " +y)
							time.sleep(.5)
						ssh_channel.send("\nsnmp-server host inside 159.140.177.127 community 7rAq@+ef\n")
						time.sleep(.5)
						ssh_channel.send("exit\n")
						time.sleep(.5)
						ssh_channel.send("wr mem\n")
						time.sleep(10)
						ssh_channel.send("exit\n")
						output = ssh_channel.recv(65535)
						
						print output
						
						completed.append(SD_Network.devicenames[j])
						a1 = open ("SNMP.txt","a")
						a1.write(output)
						
					if "snmp-server host outside 159.140.176.17 poll community 7rAq@+ef" not in output3	and "snmp-server host inside 159.140.176.17 poll community 7rAq@+ef" not in output4:			
						print(Fore.RED + "\nThe string not found\n")
						not_found.append(SD_Network.devicenames[j])
					
		except:
			print(Fore.RED + "\nUnable to login\n")
			no_login.append(SD_Network.devicenames[j])
													
		ssh.close()
		
	print (Fore.GREEN + "Completed count: "+str(len(completed)))
	print (Fore.GREEN + "Completed list: "+str(completed) +"\n")
	
	print (Fore.RED + "String not found count: "+str(len(not_found)))
	print (Fore.RED + "String not found list: "+str(not_found) +"\n")
	
	print (Fore.RED + "Standby Firewalls count : "+str(len(standby)))
	print (Fore.RED + "Standby Firewalls list: "+str(standby) + "\n")
	
	print (Fore.RED + "No login count : "+str(len(no_login)))
	print (Fore.RED + "No login list: "+str(no_login) +"\n")
	
	
SD_Network()
