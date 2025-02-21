NAMESPACE = {
  "ipi-interface": "http://www.ipinfusion.com/yang/ocnos/ipi-interface",
  "ipi-if-ip": "http://www.ipinfusion.com/yang/ocnos/ipi-if-ip",
  "ipi-network-instance": "http://www.ipinfusion.com/yang/ocnos/ipi-network-instance",
  "ipi-bridge": "http://www.ipinfusion.com/yang/ocnos/ipi-bridge",
  "ipi-vlan": "http://www.ipinfusion.com/yang/ocnos/ipi-vlan",
  "ipi-port-vlan": "http://www.ipinfusion.com/yang/ocnos/ipi-port-vlan"
}

VLAN_CREATION_STRING = """
<config>
    <network-instances xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-network-instance"> 
        <network-instance>
            <instance-name></instance-name>
            <instance-type>l2ni</instance-type>
            <config>
                <instance-name></instance-name>
                <instance-type>l2ni</instance-type>
            </config>
            <bridge xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-bridge">
                <config>
                    <protocol></protocol>
                </config>
                <bridge-ports>
                    <interface>
                        <name></name>
                        <config>
                            <name></name>
                        </config>
                    </interface>
                </bridge-ports>
                <vlans xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-vlan">
                    <vlan>
                        <vlan-id></vlan-id>
                        <config>
                            <vlan-id></vlan-id>
                        </config>
                        <customer-vlan>
                            <config>
                                <type>customer</type>
                                <state></state>
                            </config>
                        </customer-vlan>
                    </vlan>
                </vlans>
            </bridge>
        </network-instance>
    </network-instances>
</config>
"""

INTERFACES_CONFIG = """
<config>
    <interfaces xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface"> 
        <interface> 
            <!-- interface name -->
            <name></name> 
            <config> 
                <name></name> 
                <!-- converts interface to switchport --> 
                <enable-switchport></enable-switchport>
            </config>
            <port-vlan xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-port-vlan"> 
                <switched-vlans> 
                    <switched-vlan>
                        <!-- switchport mode --> 
                        <interface-mode></interface-mode> 
                        <config> 
                            <interface-mode></interface-mode> 
                        </config> 
                        <vlans> 
                            <config> 
                                    <!-- VLAN ID to associate with port -->
                                    <vlan-id></vlan-id>
                            </config> 
                        </vlans> 
                    </switched-vlan> 
                </switched-vlans> 
            </port-vlan> 
        </interface> 
    </interfaces>
</config>
"""