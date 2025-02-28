NAMESPACE = {
  "ipi-interface": "http://www.ipinfusion.com/yang/ocnos/ipi-interface",
  "ipi-if-ip": "http://www.ipinfusion.com/yang/ocnos/ipi-if-ip",
  "ipi-network-instance": "http://www.ipinfusion.com/yang/ocnos/ipi-network-instance",
  "ipi-bridge": "http://www.ipinfusion.com/yang/ocnos/ipi-bridge",
  "ipi-vlan": "http://www.ipinfusion.com/yang/ocnos/ipi-vlan",
  "ipi-port-vlan": "http://www.ipinfusion.com/yang/ocnos/ipi-port-vlan"
}

L2_VLAN_CREATION_STRING = """
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

L3_VLAN_CREATION_STRING = """
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
                <vlans xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-vlan">
                    <vlan>
                        <vlan-id></vlan-id>
                        <config>
                            <vlan-id></vlan-id>
                        </config>
                        <customer-vlan>
                            <config>
                                <type>customer</type>
                            </config>
                        </customer-vlan>
                    </vlan>
                </vlans>
            </bridge>
        </network-instance>
    </network-instances>
</config>
"""

BIND_INTERFACE_TO_BRIDGE_CONFIG = """
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
                <bridge-ports>
                    <interface>
                        <name></name>
                        <config>
                            <name></name>
                        </config>
                    </interface>
                </bridge-ports>
            </bridge>
        </network-instance>
    </network-instances>
</config>
"""

BIND_L2_VLAN_TO_INTERFACE = """
<config>
    <interfaces xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface"> 
        <interface> 
            <name></name> 
            <config> 
                <name></name> 
                <enable-switchport></enable-switchport>
            </config>
            <port-vlan xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-port-vlan"> 
                <switched-vlans> 
                    <switched-vlan>
                        <interface-mode></interface-mode> 
                        <config> 
                            <interface-mode></interface-mode> 
                        </config> 
                        <vlans> 
                            <config> 
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

BIND_L3_VLAN_TO_INTERFACE = """
<config>
  <interfaces xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface">
        <interface>
            <name></name>
            <config>
                <name></name>
                <enable-switchport></enable-switchport>
            </config>
            <port-vlan xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-port-vlan">
                <switched-vlans>
                    <switched-vlan>
                        <interface-mode></interface-mode>
                        <config>
                            <interface-mode></interface-mode>
                        </config>
                        <allowed-vlan>
                            <config>
                                <allowed-vlan-id></allowed-vlan-id>
                            </config>
                        </allowed-vlan>
                    </switched-vlan>
                </switched-vlans>
            </port-vlan>
        </interface>
    </interfaces>
</config>
"""

INTERFACE_CONFIG = """
<config>
    <interfaces xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface">
        <interface>
            <name></name>
            <config>
                <name></name>
            </config>
            <ipv4 xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-if-ip"> 
                <config> 
                    <primary-ip-addr></primary-ip-addr> 
                </config> 
            </ipv4>
        </interface>
    </interfaces>
</config>
"""