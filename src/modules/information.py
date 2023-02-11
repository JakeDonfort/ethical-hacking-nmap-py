from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, gethostbyaddr, getaddrinfo, create_connection
from platform import system, release, machine
from bs4 import BeautifulSoup
from random import choice
from requests import get
from time import sleep
from json import load
from re import search
from sys import exit
import socks

#COLORS
wb = "\033[1;97m"    #white bold
w  = "\033[0;37m"    #white
yb = "\033[1;93m"    #yellow bold
y  = "\033[0;33m"    #yellow
c  = "\033[1;96m"    #cyan
g  = "\033[0;32m"    #green
n  = "\033[0;0m"     #normal color
r  = "\033[0;31m"    #red
bg = "\033[1;97;42m" #background green with white font 


class Information:
    def __init__(
        self, ip_host=None, host=None, port=None, proxy=None, app_info=None, 
        service_name=None, data=None, error=None, type_ip=None
    ):
        self.ip_host = ip_host
        self.host = host
        self.port = port 
        self.proxy = proxy
        self.data = data 
        self.type_ip = type_ip
        self.app_info = app_info
        self.service_name = service_name
        
        
    def get_app_info(self):
        info = {
            'server': {},
            'version': {}
        }
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/90.0.864.48",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15",
        ]
        
        try:
            if self.proxy:
                socks.set_default_proxy(socks.SOCKS5, self.proxy[0], int(self.proxy[1]), True)
                request = socks.socksocket()
                
            if self.type_ip == 'ipv4':
                request = socket(AF_INET, SOCK_STREAM)
                    
            elif self.type_ip == 'ipv6':
                request = socket(AF_INET6, SOCK_STREAM)
            
            with request as socket_info:
                socket_info.connect((self.host, self.port))
                socket_info.settimeout(10)
                
                user_agent = choice(user_agents)
                system_info = f'({system()} {release()}; {machine()})'
                
                app_info = f'MyApp/1.0'
                
                user_agent = f'{user_agent} {app_info} {system_info}'
             
                request = f"GET / HTTP/1.0\r\nHost: {self.host}\r\nUser-Agent: {user_agent}\r\nAccept: */*\r\nAccept-Encoding: gzip, deflate\r\nConnection: close\r\n\r\n".encode("utf-8")
        
                socket_info.sendall(request)
                response = b"" #byte
               
                while True:
                    data = socket_info.recv(2024)
                  
                    if not data:
                        break
                  
                    response += data
        
            response = response.decode("utf-8")
            lines = response.split("\r\n")
            
            for line in lines:
                if "X-Powered-By" in line or "X-App-Version" in line:
                    info["version"] = line.replace("X-Powered-By:", "").replace("X-Powered-By:", "").strip()
                    
                if "Server" in line and not "X-Server-Cache" in line:
                    info["server"] = line.replace("Server:", "").strip()
        
            return info

        except KeyboardInterrupt:
            exit()
            
        except Exception as error:
            if "[Errno 104] Connection reset by peer" in str(error):
                pass 
            
            elif "'utf-8' codec can't decode byte 0x8b in position 589" in str(error):
                pass 
            
            elif "[Errno 7]":
                pass
    
            else:
                print("Error in information.py - line 115: ", error)
                
                
    def get_service_name_port(self):
        tcp_info_file = './src/assets/ports_info_tcp_IANA.json'
   
        port = str(self.port)
        
        try:
        	with open(tcp_info_file, "r") as archive:
        		data = load(archive)
        		
        	if (port in data['tcp']):
        		service_name = data['tcp'][port]['Service Name']
        		return f'{service_name}' 
        	
        	else:
        	    return

        except KeyboardInterrupt:
            exit()
            
        except Exception as error:
            print(error)
            
            
    def get_all_port_info(self):
        try:
            service_name_port = self.service_name
            app_info = self.app_info
            port = f'{str(self.port)}/tcp'
    
            info_data = False
           
            if app_info:
                if app_info["server"] and app_info["version"]:
                    port_info = [f'  {port:<9}  open   {service_name_port:<14} {app_info["server"]:<19} {app_info["version"]}']
                    info_data = "server version"
                    
                elif app_info["server"]:
                    port_info = [f'  {port:<9}  open   {service_name_port:<14} {app_info["server"]}']
                    info_data = "server"
                    
                elif app_info["version"]:
                    port_info = [f'  {port:<9}  open   {service_name_port:<14} {app_info["version"]}']
                    info_data = "version"
                
                else:
                    port_info = [f'  {port:<9}  open   {service_name_port:<14}']
                    
            else:
                port_info = [f'  {port:<9}  open   {service_name_port:<14}']
            
            return info_data, port_info
        
        except KeyboardInterrupt:
            exit()
            
        except Exception as error:
            if "unsupported format string passed to NoneType" in str(error):
                exit()
                
            else:
                print(">>> Error: ", error)
            
            
    def get_resolver_host(self):
        try:
            data = set()
            ips  = str()
    
            results = getaddrinfo(self.host, None)
     
            for result in results:
                data.add(result[4][0])
                
            for ip in data:
                ips += f'{ip} '
    
            ips = ips.replace(self.ip_host, "")
             
            if len(ips) >= 7:#0.0.0.0
                return ips 
            else:
                return

        except KeyboardInterrupt:
            exit()
            
        except:
            return 
        
        
    def get_rdns(self):
        try:
            hostname, _, _ = gethostbyaddr(self.ip_host)
            return hostname
        
        except KeyboardInterrupt:
            exit()
            
        except:
            return  
        
        
    def get_check_network(self):
        attempt = -1
        
        try:
            while True:
                host = "google.com"
                
                try:
                    result = create_connection((host, 80), timeout=5)
                    return True

                except:
                    attempt += 1
                    
                    if self.data == "scan":
                        if attempt == 10:
                            print("\nThe internet is unstable, this may affect scan performance!\n")
                            return False
                    else:
                        if attempt == 0:
                            print("\nTrying to reestablish the connection...\n")
                            attempt += 1
                            
                        elif attempt == 10:
                            print("\nNo internet connection or your network must be unstable\n")
                            return False 
                    
        except KeyboardInterrupt:
            exit()
                    
             
    def get_proxy(self):
        proxy_api_url = 'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=1000&country=US&ssl=all&anonymity=elite' 
        
        try:
            response = get(proxy_api_url)
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            soup = soup.prettify()
            data = soup.split()[0].replace(":", " ").split()#To return all proxies ips -> soup.split()
            
            return data
        
        except KeyboardInterrupt:
            exit()
            
        except:
            print("\nAn error occurred while trying to use the proxy\n") 
            
            
    def get_error_info(self):
        error = self.error
        
        try:
            if "timed out" in str(error):
                pass 
                
            elif '[Errno 7]' in error:
                print('\nNo internet connection, please try again\n')
    
            elif "unhashable type: 'list'" in error:
                pass
    
            elif "'utf-8' codec can't decode" in error:
                pass
    
            elif "0x01: General SOCKS server failure" in error:
                print("\n>>> There was a connection error, please check if your internet is stable\n")
                exit()
                
            elif "0x04: Host unreachable" in error:
                pass
               
            elif "Connection closed unexpectedly" in error:
                print("\nConnection closed unexpectedly, aborting...")
                eixt()
          
            elif "0x03: Network unreachable" in error:
                exit()
                
            else:
                print("Error: ", error)
                
        except KeyboardInterrupt:
            exit()
            
            
    def show_menu_info(self):
        print("\n---------- --------- -------- ------- ------ ---- -- -  - -- -")
        
        print(f"{wb}| host: {r}The use of the host flag is mandatory{n}\n")
        print(f"    {c}--h{n} <host>\n")
        print(f"    {y}Example:\n")
        print(f"      {c}--h{wb} ana.com    {n}or    {c}--h {wb}104.21.52.8 ")
        print(f"        {w}host name              address ip\n")
        
        print(f"{wb}| port:{r} The use of the flag port is mandatory{n}\n")
        print(f"    {c}--p{n} <port> \n")
        print(f"    {y}Example:  \n")
        print(f"        {c}--p{wb} 22      {n}or    {c}--p{wb}  22-443             {n}or        {c}--p{wb}  all")
        print(f"        {w}one port        range [22, 23... 443]         all ports (0... 65535) \n\n")
        
        print(f"{wb}| proxy: {g}Using the proxy flag is optional{n}\n")
        print(f"    {c}--proxy{n} <proxy_host:proxy_port>  \n")
        print(f"    {y}Example: \n")
        print(f"        {c}--proxy {n}72.221.172.203:4145      or    {c}--proxy{n}  auto ")
        print(f"              {w}proxy host  and : port         use automatic proxy \n")
     
        print(f"    {yb}ATTENTION:\n")
        print(f"         {w}Using a {y}proxy{w} can slow down the scanner, and malfunctions")
        print(f"         may occur and sometimes not show open ports!{n}\n\n")
      
        print(f"| {bg}How to use:{n}\n")
        print(f"    {c}--h {wb}ana.com      {c}--p {wb}80      {c}--proxy   {wb}auto ")
        print(f"    {c}--h {wb}104.21.52.8  {c}--p {wb}22-80   {c}--proxy   {wb}auto ")
        print(f"    {c}--h {wb}bancocn.com  {c}--p {wb}22-443   ")
        print(f"    {c}--h {wb}ana.com      {c}--p {wb}all     {c}--proxy   {wb}72.221.172.203:4145")
        
        print("---------- --------- -------- ------- ------ ---- -- -  - -- -\n")
