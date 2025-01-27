import ncclient
from ncclient import manager
import os
import xml.etree.ElementTree as ET


def fetch_interfaces(host: str, username: str, password: str):

    m = manager.connect(host=host, username=username, password=password, hostkey_verify=False)

    ns = {"ipi-interface": "http://www.ipinfusion.com/yang/ocnos/ipi-interface"}

    netconf_filter = """
    <filter type="xpath">/ipi-interface:interfaces/ipi-interface:interface</filter>
    """
    
    result = m.get(filter=netconf_filter)

    tree = ET.fromstring(result.xml)

    interfaces = tree.findall(".//ipi-interface:interface", namespaces=ns)

    for interface in interfaces:
        name = interface.find(".//ipi-interface:name", namespaces=ns).text
        
        oper_status = interface.find(".//ipi-interface:state/ipi-interface:oper-status", namespaces=ns).text
        
        admin_status = interface.find(".//ipi-interface:state/ipi-interface:admin-status", namespaces=ns).text
        
        print(f"Interface: {name}, Operational Status: {oper_status}, Admin Status: {admin_status}\n")

def main():
    host = os.getenv("IP_ADDR")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    fetch_interfaces(host, username, password)

if __name__ == "__main__":
    main()