import lxml.etree as et
import requests
import os
import subprocess
import json


if __name__ == '__main__':
    # Use metadata to query Azure & parse the Json file to get the resource group of this VM
    x =  subprocess.check_output('curl -H Metadata:true --noproxy "*" "http://169.254.169.254/metadata/instance?api-version=2020-09-01" | jq .', shell=True)
    x = x.decode("utf-8")
    keyVal = 'resourceGroupName'
    resourceGroupName = ''
    toParse = json.loads(x)

    print(toParse['compute']['resourceGroupName'])

    if 'compute' in toParse:
        if keyVal in toParse['compute']:
            resourceGroupName = toParse['compute'][keyVal]

 
    headerTxt = '<user-mapping>\n'
    txt = '''
                <authorize
                        username="arsiem"
                        password="Arsiem2020!!">
                    <connection name="Default-Server-SSH">
                        <protocol>ssh</protocol>
                        <param name="hostname"></param>
                        <param name="port">22</param>
                    </connection>
                    <connection name="Default-Server-RDP">
                        <protocol>rdp</protocol>
                        <param name="hostname"></param>
                    <param name="port">3389</param>
                    </connection>
                </authorize>
            '''
    closerTxt = '</user-mapping>'

    result = headerTxt
    cwd = os.getcwd()
    # LOAD XSL SCRIPT
    x = requests.get('https://api-for-guacips.azure-api.net/manual/paths/invoke?name=%s' %resourceGroupName)
    ipdata = x.json()
    for i in range(len(ipdata)):
        if 'guac' not in ipdata[i]:
            # FORMAT STRING VALUE
            x = ipdata[i].split('|')
            print(x)
            newList = x[0].split('-')
            name = newList[0].strip()
            ip = x[1]
            data = et.XSLT.strparam(ip.strip())

            xml = et.fromstring(txt.replace('Default', name))
            xsl = et.parse('XSLTScript.xsl')
            transform = et.XSLT(xsl)

            # PASS PARAMETER TO XSLT            
            result += str(transform(xml, new_ip=data))
    result += closerTxt
    # SAVE XML TO FILE
    with open('user-mapping.xml', 'w') as f:
        f.write(result)
