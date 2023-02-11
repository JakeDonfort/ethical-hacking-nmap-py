from sys import argv, exit
from time import time

from src.modules import information as info
from src.modules import validation as vl
from src.modules import scanner as scan

proxy = False


if __name__ == "__main__":
    try:
        info = info.Information(data='main')
        ethernet = info.get_check_network()
      
        if ethernet:
            flags = str(argv).lower().replace("', '", "").replace("--", " --").replace("['", "").replace("']", "").split()
             
            if len(flags) > 1:
                validation = vl.Validation(flags=flags)
                host, port, proxy = validation.get_flags()
                
                try:      
                    if host and port and not proxy:
                        data = vl.Validation(host, port)
                        host, port = data.get_address()
                        scanner = scan.PortScanner(host, port)
                        scanner.scan()
                        
                    elif host and port and proxy:
                        data = vl.Validation(host, port, proxy)
                        host, port, proxy = data.get_address()
           
                        scanner = scan.PortScanner(host, port, proxy)
                        scanner.scan()
                        
                    else:
                        print(f'\n>>> Missing host or port\n')
                        exit()
                        
                except NameError:
                    print(f'\n>>> Error, make sure you passed the host and port correctly\n')
                 
            else:
                data = vl.Validation()
                host, port = data.get_address()
                   
                while True: 
                 
                    try: 
                        answer = input('\nProxy? [Y/N]: ').strip().lower()[0]
                        
                        if answer == 'n':
                            scanner = scan.PortScanner(host, port) 
                            scanner.scan()
                            break 
                        
                        elif answer == 'y':
                            data = vl.Validation(host=None, port=None, proxy="auto")
                            proxy = data.get_address()
                            scanner = scan.PortScanner(host, port, proxy)
                            scanner.scan()
                            break
                         
                        else: 
                         	print('>>> Invalid Parameter')
                     
                    except KeyboardInterrupt:
                        exit()
        else:
            pass 
         
    except KeyboardInterrupt:
        exit()
