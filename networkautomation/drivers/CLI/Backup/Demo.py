from netmiko import ConnectHandler 
from datetime import datetime
#1. Định nghĩa hàm backup
bk_device = {} 
tftpserver = "192.168.0.48" 

def cisco_ios(txt): # hàm backup cho cisco ios
	
	cmd = "copy running-config tftp:"
	filename = txt
	
	net_connect = ConnectHandler(**bk_device)

	output = net_connect.send_command_timing(cmd)
	if "Address or name of remote host []" in  output:
		output += net_connect.send_command_timing(tftpserver)
	if "Destination filename" in output:
		output += net_connect.send_command_timing(filename)

	print(output)
	print("-" * 80)	


def cisco_asa(txt): #Hàm backup cho cisco_asa
	print("Chua viet cisco_asa")

def juniper_srx(txt):#Hàm backup cho juniper_srx
	print("Chua viet juniper_srx")

#2. Mở file device_list.csv. Định nghĩa file backup và gọi hàm backup tương ứng với từng vender
with open ("device_list.csv","r") as rfile: # mở file

	keys = rfile.readline().split(",")
	values = rfile.read() 
for values in values.splitlines(): 
	values = values.split(",") 
	for i in range(1,len(keys)-1,1): 
		bk_device[keys[i]] = values[i]  
		
	print(f"Dang ket noi vao IP:'{values[1]}' voi Username: '{values[2]}'")	

	now = datetime.now().strftime("%Y-%b-%d_%H%M%S") # lấy ngày giờ hiện tại (thoigian)
	filename = now + "_" + values[4] + "_" + values[1] # tên file backup là: thoigian_vendor_IPAddr

	if values[4] == "cisco_ios" : 
		cisco_ios(filename) # gọi hàm backup cisco_ios đã được định nghĩa trước đó
	elif values[4] == "cisco_asa" :
		cisco_asa(filename)
	elif values[4] == "juniper_srx" :
		juniper_srx(filename)
	else:	
		print("thiet bi khac")