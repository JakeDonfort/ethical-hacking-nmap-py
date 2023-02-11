from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, gethostbyname, getservbyport
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, date
from time import time, perf_counter, sleep
from threading import Thread
from sys import exit
import socks

from .validation import Validation
from .information import Information
from ..assets.editable import max_workers

date = date.today()
now  = datetime.now()
hour = now.strftime("%H:%M")

latency = False

#colors 
r = '\033[1;37;41m' # background red, font white 
w = '\033[1;37m'    # font white bold
n = '\033[0m'       # font normal color 


class PortScanner:
    def __init__(self, host, port, proxy=None):
        self.host = host
        self.port = port 
        self.proxy = proxy 
        
        self.port_info  =  set()
        self.result_scan = list()
        
        self.open_ports = list()
        self.cont_ports = int(0)
        self.host_up = int(0)
        
    
    def scan(self):
        try:
            global date, hour, max_workers

            try:
                ip_host = gethostbyname(self.host)
                info = Information(host=self.host, ip_host=ip_host)
                
                outer_ips = info.get_resolver_host()
                rdns = info.get_rdns()
            
            except:
                ip_host = self.host
                info = Information(host=self.host, ip_host=self.host)
              
                outer_ips = info.get_resolver_host()
                rdns = info.get_rdns()
                
            finally:
                self.host_up +=1 
                
            print(f'\nStarting Scan (github) at {w}{date}  {hour}{n}')
            print(f'Scan report for {w}{self.host} ({ip_host}){n}')
            
            if rdns:
            	print(f'rDNS record for {w}{ip_host}{n}: {w}{rdns}{n}')
            
            if outer_ips:
            	print(f"Other addresses for {w}{self.host}{n} (not scanned): {outer_ips}")
            	
            start_time = time() 
            
            try:
                with ThreadPoolExecutor(max_workers = max_workers) as executor:
                    cont_port: int = 0
                    
                    for port in self.port:
                        if cont_port == 32_000:
                            cont_port = 1
                            
                            info = Information(data='scan')
                            
                            if not info.get_check_network(self):
                                exit()
                        try:
                            if self.proxy:
                                executor.submit(self.scan_port, self.host, int(port), self.proxy)
               
                            else:
                                executor.submit(self.scan_port, self.host, int(port))
                       
                        except KeyboardInterrupt:
                            exit()
                        
                        except:
                            print("\nA processing error occurred. Please try again later\n")
                            exit()
                            
                        finally:
                            cont_port += 1
                            
            except MemoryError:
                print('\n>>> Error in treading, decrease the value of treading in "/src/assets/editable.py\n"')
                exit()
                
            except KeyboardInterrupt:
                print("\n>>> Exiting... \n")
                exit()
                
            except Exception as error:
                Information(error=error)
                Information.get_error_info()
                    
            end_time = time()
            calc_time = (end_time - start_time)
            total_time = str(round(calc_time, 2))
            
            print(f'Host is up ({latency:.2f}s latency).')
            
            if self.open_ports:
                if "server version" in self.port_info:
                    print(f'\n  {r}PORT{n}      {r}STATE{n}   {r}SERVICE{n}        {r}SERVER{n}              {r}VERSION{n}')
                                    
                elif "server" in self.port_info:
                    print(f'\n  {r}PORT{n}      {r}STATE{n}   {r}SERVICE{n}        {r}SERVER{n}')
                
                elif "version" in self.port_info:
                    print(f'\n  {r}PORT{n}      {r}STATE{n}   {r}SERVICE{n}        {r}VERSION{n}')
                
                else:
                    print(f'\n  {r}PORT{n}      {r}SATATE{n}  {r}SERVICE{n}')
                 
                for results in self.result_scan:
                    for result in results:
                        print(str(result).replace("['", "").replace("']", ""), end="")
                    print()
                    
            else:
                if self.proxy:
                    print('\n  No open tcp port(s). Possible errors, ethernet, firewall or proxy(90%)!')
                
                else:
                    print("\n  No open tcp port(s)!")
                
            print(f'\nTotal {w}{self.cont_ports}{n} port(s) scanned, Total {w}{len(self.open_ports)}{n} open ports.')
            print(f'Scan done: {len(self.host.split())} IP address ({self.host_up} host up)  scanned in {w}{total_time}{n} seconds')
            
        except KeyboardInterrupt:
            exit()
            
        except Exception as error:
            Information(error=error)
            Information.get_error_info()
        
    
    def scan_port(self, host, port, proxy=None):
        global latency 
        
        data = Validation(host)
        ip = data.get_ip_type()
        app_info = False

        try:
            if self.proxy:
                socks.set_default_proxy(socks.SOCKS5, self.proxy[0], int(self.proxy[1]), True)#True ...
                scan_sock = socks.socksocket()
                scan_sock.settimeout(4.0)
            
            if ip == 'ipv4':
                scan_sock = socket(AF_INET, SOCK_STREAM)
                    
            elif ip == 'ipv6':
                scan_sock = socket(AF_INET6, SOCK_STREAM)
                
            scan_sock.settimeout(1.0)
          
            start_lt = time()
            connection_code = scan_sock.connect_ex((host, port))
            end_lt = time()
           
            if not latency:
                latency = (end_lt - start_lt)
              
            if (connection_code == 0):
                if port == 80 or port == 443:
                    info = Information(host=host, port=port, proxy=self.proxy, type_ip=ip)
                    app_info = info.get_app_info()
                
                try:
                    service_name = getservbyport(port)
                    info = Information(app_info=app_info, port=port, service_name=service_name)
                    return_all_info = info.get_all_port_info()
                    
                    self.port_info.add(return_all_info[0])
                    self.result_scan += return_all_info[1]
            
                except KeyboardInterrupt:
                    exit()
              
                except:
                    try:
                        service = Information(port=port)
                        service_name = service.get_service_name_port()
                        
                        info = Information(port=port, app_info=app_info, service_name=service_name)
                        return_all_info = info.get_all_port_info()
                        
                        self.port_info.add(return_all_info[0])
                        self.result_scan += return_all_info[1]
                    
                    except KeyboardInterrupt:
                        exit()
                        
                    except:
                        return_data = [[f'  {port}/tcp   open  None']]
                        self.port_info.add(return_data[0])
                        self.result_scan += return_data[1]
                    
                finally:
                    self.open_ports.append(port)

            if not self.proxy:
                self.cont_ports += 1
                
            scan_sock.close()
            
        except KeyboardInterrupt:
            exit() 
            
        except Exception as error: 
            Information(error=error)
            Information.get_error_info()
                
        finally:
            if self.proxy:
                self.cont_ports += 1

