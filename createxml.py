import lxml.etree as et
import requests
import os

txt = '''<user-mapping>
            <authorize
                    username="arsiem"
                    password="Arsiem2020!!">
                <connection name="Ubuntu-Server">
                    <protocol>ssh</protocol>
                    <param name="hostname"></param>
                    <param name="port">22</param>
                </connection>

                <connection name="Windows Server">
                    <protocol>rdp</protocol>
                    <param name="hostname"></param>
                <param name="port">3389</param>
                </connection>
            </authorize>
        </user-mapping>'''

cwd = os.getcwd()
# LOAD XSL SCRIPT
x = requests.get('https://api-for-guacips.azure-api.net/manual/paths/invoke?name=Packet-Analysis-Test1')
ipdata = x.json()
xml = et.fromstring(txt)
xsl = et.parse('XSLTScript.xsl')
transform = et.XSLT(xsl)

# PASS PARAMETER TO XSLT
n = et.XSLT.strparam(ipdata[0])
result = transform(xml, new_ip=n)

print(result)


# SAVE XML TO FILE
with open('user-mapping.xml.xml', 'wb') as f:
    f.write(result)
