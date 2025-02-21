import xml.etree.ElementTree as ET

from flask import Blueprint, request, jsonify, redirect, render_template
from ncclient import manager

from constants import VLAN_CREATION_STRING, NAMESPACE, INTERFACES_CONFIG

vlan_bp = Blueprint("vlans", __name__, url_prefix="/vlans")


@vlan_bp.route("/create-vlan", methods=["GET", "POST"])
def create_vlan():
    if request.method == "GET":
        return render_template("vlans.html")

    if request.method == "POST":

        bridge_id = request.form.get("bridge-id")
        bridge_label = request.form.get("bridge-label")
        bridge_protocol = request.form.get("bridge-protocol")
        vlan_id = request.form.get("vlan-id")
        vlan_state = request.form.get("vlan-state")
        switchport_mode = request.form.get("switchport-mode")
        interface_name = request.form.get("interface-name")

        VLAN_CONFIG = ET.fromstring(VLAN_CREATION_STRING)
        INTERFACE_CONFIG = ET.fromstring(INTERFACES_CONFIG)

        bridge_id_tag = VLAN_CONFIG.find(".//ipi-network-instance:instance-name", namespaces=NAMESPACE)
        bridge_label_tag = VLAN_CONFIG.find(".//ipi-network-instance:config/ipi-network-instance:instance-name", namespaces=NAMESPACE)

        vlan_id_tag = VLAN_CONFIG.find(".//ipi-vlan:vlan/ipi-vlan:vlan-id", namespaces=NAMESPACE)
        vlan_state_id_tag = VLAN_CONFIG.find(".//ipi-vlan:vlan/ipi-vlan:config/ipi-vlan:vlan-id", namespaces=NAMESPACE)
        vlan_state_tag = VLAN_CONFIG.find(".//ipi-vlan:vlan/ipi-vlan:config/ipi-vlan:state", namespaces=NAMESPACE)

        bridge_protocol_tag = VLAN_CONFIG.find(".//ipi-bridge:config/ipi-bridge:protocol", namespaces=NAMESPACE)
        bridge_interface_tag = VLAN_CONFIG.find(".//ipi-bridge:bridge-ports/ipi-bridge:interface/ipi-bridge:name", namespaces=NAMESPACE)
        bridge_interface_config_tag = VLAN_CONFIG.find(".//ipi-bridge:bridge-ports/ipi-bridge:interface/ipi-bridge:config/ipi-bridge:name", namespaces=NAMESPACE)

        interface_tag = INTERFACE_CONFIG.find(".//ipi-interface:interface/ipi-interface:name", namespaces=NAMESPACE)
        interface_config_tag = INTERFACE_CONFIG.find(".//ipi-interface:interface/ipi-interface:config/ipi-interface:name", namespaces=NAMESPACE)

        switchport_mode_tag = INTERFACE_CONFIG.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:interface-mode", namespaces=NAMESPACE)
        switchport_mode_config_tag = INTERFACE_CONFIG.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:config/ipi-port-vlan:interface-mode", namespaces=NAMESPACE)
        switchport_vlan_config_tag = INTERFACE_CONFIG.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:vlans/ipi-port-vlan:config/ipi-port-vlan:vlan-id", namespaces=NAMESPACE)

        if bridge_id_tag is not None: bridge_id_tag.text = bridge_id
        if bridge_label_tag is not None: bridge_label_tag.text = bridge_label

        if vlan_id_tag is not None: vlan_id_tag.text = vlan_id
        if vlan_state_id_tag is not None: vlan_state_id_tag.text = vlan_id
        if vlan_state_tag is not None: vlan_state_tag.text = vlan_state

        if bridge_protocol_tag is not None: bridge_protocol_tag.text = bridge_protocol
        if bridge_interface_tag is not None: bridge_interface_tag.text = interface_name
        if bridge_interface_config_tag is not None: bridge_interface_config_tag.text = interface_name

        if interface_tag is not None: interface_tag.text = interface_name
        if interface_config_tag is not None: interface_config_tag.text = interface_name

        if switchport_mode_tag is not None: switchport_mode_tag.text = switchport_mode
        if switchport_mode_config_tag is not None: switchport_mode_config_tag.text = switchport_mode
        if switchport_vlan_config_tag is not None: switchport_vlan_config_tag.text = vlan_id

        NEW_VLAN_CONFIG = ET.tostring(VLAN_CONFIG, encoding="unicode")
        NEW_INTERFACE_CONFIG = ET.tostring(INTERFACE_CONFIG, encoding="unicode")

        with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
            try:
                vlan_result = m.edit_config(target="candidate", config=NEW_VLAN_CONFIG)
                m.commit()
                try:
                    interface_result = m.edit_config(target="candidate", config=NEW_INTERFACE_CONFIG)
                    m.commit()
                except Exception as i_e:
                    print(i_e)
                finally:
                    return redirect("/vlans/create-vlan")

            except Exception as e:
                print(e)

        return redirect("/vlans/create-vlan")