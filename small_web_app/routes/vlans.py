import xml.etree.ElementTree as ET

from flask import Blueprint, request, jsonify, redirect, render_template
from ncclient import manager

from constants import L3_VLAN_CREATION_STRING, L2_VLAN_CREATION_STRING, NAMESPACE

vlan_bp = Blueprint("vlans", __name__, url_prefix="/vlans")


@vlan_bp.route("/create-vlan", methods=["GET", "POST"])
def create_vlan():
    NEW_VLAN_CONFIG = None

    if request.method == "GET":
        return render_template("vlans.html")

    if request.method == "POST":

        bridge_id = request.form.get("bridge-id")
        bridge_protocol = request.form.get("bridge-protocol")
        vlan_id = request.form.get("vlan-id")
        vlan_state = request.form.get("vlan-state")
        vlan_layer = request.form.get("vlan-layer")

        VLAN_CONFIG = ET.fromstring(L3_VLAN_CREATION_STRING) if vlan_layer == "layer-3" else ET.fromstring(L2_VLAN_CREATION_STRING)

        bridge_id_tag = VLAN_CONFIG.find(".//ipi-network-instance:instance-name", namespaces=NAMESPACE)
        bridge_id_config_tag = VLAN_CONFIG.find(".//ipi-network-instance:config/ipi-network-instance:instance-name", namespaces=NAMESPACE)

        vlan_id_tag = VLAN_CONFIG.find(".//ipi-vlan:vlan/ipi-vlan:vlan-id", namespaces=NAMESPACE)
        vlan_config_id_tag = VLAN_CONFIG.find(".//ipi-vlan:vlan/ipi-vlan:config/ipi-vlan:vlan-id", namespaces=NAMESPACE)
        vlan_state_tag = VLAN_CONFIG.find(".//ipi-vlan:vlan/ipi-vlan:customer-vlan/ipi-vlan:config/ipi-vlan:state", namespaces=NAMESPACE)

        bridge_protocol_tag = VLAN_CONFIG.find(".//ipi-bridge:config/ipi-bridge:protocol", namespaces=NAMESPACE)

        if bridge_id_tag is not None: bridge_id_tag.text = bridge_id
        if bridge_id_config_tag is not None: bridge_id_config_tag.text = bridge_id

        if vlan_id_tag is not None: vlan_id_tag.text = vlan_id
        if vlan_config_id_tag is not None: vlan_config_id_tag.text = vlan_id
        if vlan_state_tag is not None: vlan_state_tag.text = "disable" if vlan_state == None else vlan_state

        if bridge_protocol_tag is not None: bridge_protocol_tag.text = bridge_protocol
        
        NEW_VLAN_CONFIG = ET.tostring(VLAN_CONFIG, encoding="unicode")

        with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
            try:
                vlan_result = m.edit_config(target="candidate", config=NEW_VLAN_CONFIG)
                m.commit()
            except Exception as e:
                print(f"Detailed error message: {e}")

        return redirect("/interfaces/")
