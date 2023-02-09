from socket import gethostbyname, gethostbyaddr
from ipaddress import ip_address, IPv4Address, IPv6Address
from sys import exit

from .information import Information as info

#colors
y = '\033[33m'#yellow font
n = '\033[0m' #normal font 
r = '\033[31m'#ref font

class Validation:
    def __init__(self, host=None, port=None, proxy=None, flags=None):
        self.host = host 
        self.port = port 
        self.proxy = proxy 
        self.flags = flags 
        self.show_menu = False

    def get_flags(self):
        for index, flag in enumerate(self.flags):
            if '--help'in flag:
                info.show_menu_info(self)
                exit()
                    
            elif '--p' in flag and not '--proxy' in flag:
                self.port = flag.replace("--p", "")
                    
            elif '--proxy' in flag:
                self.proxy = flag.replace("--proxy", "").replace(":", " ").split()
            
            elif '--h' in flag:
                self.host = flag.replace("--h", "")
           
        return self.host, self.port, self.proxy
        
        
    def get_ip_type(self):
        try:
            try:
                ip_host = gethostbyname(self.host)
                ip_host = ip_address(ip_host)
                
            except:
                ip_host = self.host
                ip_host = ip_address(ip_host)
                
            if isinstance(ip_host, IPv4Address):
                return "ipv4"
            
            elif isinstance(ip_host, IPv6Address):
                return "ipv6"
                
        except:
            return 
            
            
    def get_address(self):
        try:
            if self.host:
                try:
                    if gethostbyname(self.host):#ipv4
                        pass
                except:
                    try:
                        if ip_address(self.host):#ipv6
                            pass
                        
                    except:
                        print(f'\n>>> Invalid host\n')
                        exit()
                    
            if self.port:
                self.port = self.port.strip().replace(" ", "").replace("-", " ").split()
                
                try:
                    if len(self.port) == 2:
                        if int(self.port[0]) <= 65535 and int(self.port[1]) <= 65535:
                            self.port  = list(map(int, self.port))
                            start = min(self.port)
                            end = max(self.port)
                            self.port  = list(range(start, end+1))
                        
                        else:
                            print(f'\n>>> Invalid port: there is no port above 65535\n')
                            exit()
                            
                    elif (len(self.port) == 1):
                        if ('all' in self.port[0]):
                            self.port = list(range(65535))
                            
                        elif int(self.port[0]) <= 65535:
                                pass
                           
                        elif int(self.port[0]) > 65535:
                            print(f'\n>>> Invalid port: there is no port above 65535\n')
                            exit()
                                                    
                        else:
                            print(f'\n>>> Invalid port\n')
                            exit()
                    else:
                        print(f"\n>>> Invalid port\n")
                        exit()
             
                except OverflowError:
                    print(f'\n>>> Invalid port: there is no port above 65535\n')
                    exit()
                    
                except Exception as error:
                    if 'invalid literal for int() with base 10' in str(error):
                        print(f'\n>>> Invalid port: cannot contain letters in the port, only "--p all"\n')
                        exit()
                
            if self.proxy:
                try: 
                    if "auto" in self.proxy:
                        self.proxy = info.get_proxy(self)
                   
                    else:
                        if gethostbyname(self.proxy[0]):
                            pass
                            
                        if self.proxy[1]:
                            pass
                             
                            try:
                                int(self.proxy[1])
                               
                            except Exception as error:
                                print(f'\n>>> Invalid port proxy\n')
                                exit()
                            
                except:
                    print(f'\n>>> Invalid host proxy\n')
                    exit()
                    
            if not self.host and not self.port and not self.proxy:
                while True:
                    try:
                        self.host = input('Host: ').strip()
                        if self.host == "":
                            continue

                        try:
                            if gethostbyname(self.host):# is ipv4
                                break

                        except:
                            try:
                                if ip_address(self.host):#is ipv6 
                                    break 
                                
                            except:
                                print(f'>>> Invalid host\n')
                           
                    except KeyboardInterrupt:
                        exit()
                    
                    except:
                        print(f'>>> Invalid host\n')
                
                while True:
                    try:
                        port = input('Port: ')
                        self.port = port.strip().replace(" ", "").replace("-", " - ").split()
                        
                        if ((len(self.port) == 1) and (self.port[0].isnumeric())):
                            break 
                        
                        elif 'all' in self.port:
                            self.port = list(range(65535))
                            break
            
                        elif ((len(self.port) == 3)  and ('-' in self.port)):
                            self.port.remove(self.port[1])
                            self.port = list(map(int, self.port))
                            start = min(self.port)
                            end = max(self.port)
                            
                            self.port  = list(range(start, end+1))
                            break
                            
                        else:
                            print(f'>>> Invalid port\n')
                            
                        try:
                            if int(self.port[0]) > 65535 or int(self.port[2]) > 65535:
                                print(f'>>> Invalid port: there is no port above 65535\n')
                      
                        except:
                            pass
                            
                    except KeyboardInterrupt:
                        exit()
                    
                    except:
                        print("\n>>> Invalid port")
                        
             
            if self.host and self.port and self.proxy:
                print(f"\nYour proxy is {y}{self.proxy[0]}:{self.proxy[1]}{n}")
                return self.host, self.port, self.proxy 
          
            elif self.host and self.port:
                return self.host, self.port
           
            elif self.proxy:
                print(f"\nYour proxy is {y}{self.proxy[0]}:{self.proxy[1]}{n}")
                return self.proxy
                
        except KeyboardInterrupt:
            exit()
