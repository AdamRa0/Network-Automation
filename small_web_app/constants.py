NAMESPACE = {
  "ipi-interface": "http://www.ipinfusion.com/yang/ocnos/ipi-interface",
  "ipi-if-ip": "http://www.ipinfusion.com/yang/ocnos/ipi-if-ip",
  "ipi-network-instance": "http://www.ipinfusion.com/yang/ocnos/ipi-network-instance",
  "ipi-bridge": "http://www.ipinfusion.com/yang/ocnos/ipi-bridge",
  "ipi-vlan": "http://www.ipinfusion.com/yang/ocnos/ipi-vlan",
  "ipi-port-vlan": "http://www.ipinfusion.com/yang/ocnos/ipi-port-vlan"
}

VLAN_CREATION_STRING = """
<network-instances xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-network-instance"> 
	<network-instance> 
        <!-- Bridge ID goes here -->
		<instance-name></instance-name> 
		<config> 
            <!-- Bridge label and bridge type go here -->
			<instance-name></instance-name> 
			<instance-type>l2ni</instance-type> 
		</config> 
		<bridge xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-bridge"> 
			<vlans xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-vlan"> 
			    <vlan> 
                <!-- VLAN ID goes here--> 
				    <vlan-id></vlan-id> 
				    <config> 
					    <vlan-id></vlan-id> 
                        <!-- state = enable or disable -->
					    <state></state> 
				    </config> 
				</vlan> 
			</vlans> 
            <!-- Bridge config -->
            <config>
                <!-- Bridge protocol -->
                <protocol></protocol> 
            </config>
            <bridge-ports> 
                <!-- associate interface with this bridge group -->
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
"""

INTERFACES_CONFIG = """
<interfaces xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface"> 
	<interface> 
        <!-- interface name -->
		<name></name> 
		<config> 
			<name></name> 
		</config>
        <!-- converts interface to switchport --> 
		<enable-switchport></enable-switchport>
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
"""