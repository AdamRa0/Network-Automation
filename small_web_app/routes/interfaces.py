from flask import Flask, jsonify, render_template, request, redirect, Blueprint
from ncclient import manager
import xml.etree.ElementTree as ET

from constants import NAMESPACE, INTERFACE_CONFIG, BIND_INTERFACE_TO_BRIDGE_CONFIG, BIND_L2_VLAN_TO_INTERFACE, BIND_L3_VLAN_TO_INTERFACE
from filter_string_provider import provide_filter_string


interface_bp = Blueprint("interfaces", __name__, url_prefix="/interfaces")


@interface_bp.route("/")
def list_interfaces():
    netconf_filter = provide_filter_string("/ipi-interface:interfaces/ipi-interface:interface")

    with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
        result = m.get(filter=netconf_filter)

    tree = ET.fromstring(result.xml)

    interfaces = tree.findall(".//ipi-interface:interface", namespaces=NAMESPACE)

    all_interfaces: list[dict[str, str]] = []

    for interface in interfaces:
        name = interface.find(".//ipi-interface:name", namespaces=NAMESPACE).text
        oper_status = interface.find(".//ipi-interface:state/ipi-interface:oper-status", namespaces=NAMESPACE).text
        admin_status = interface.find(".//ipi-interface:state/ipi-interface:admin-status", namespaces=NAMESPACE).text

        all_interfaces.append({
            "name": name,
            "oper-status": oper_status,
            "admin-status": admin_status
        })

    return render_template('interfaces.html', data=all_interfaces)

@interface_bp.route("/config-interface", methods=["POST"])
@interface_bp.route("/config-interface/<name>", methods=["GET"])
def configure_interface(name=None):

    if request.method == "GET":
        is_l2_vlan = False
        vlan_id = name.split(".")[-1]

        netconf_filter = provide_filter_string("/ipi-network-instance:instances/ipi-network-instance:instance")

        with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
            result = m.get(filter=netconf_filter)

        tree = ET.fromstring(result.xml)

        vlans = tree.findall(".//ipi-vlan:vlan", namespaces=NAMESPACE)

        for vlan in vlans:
            vlan_identifier = vlan.find(".//ipi-vlan:vlan-id", namespaces=NAMESPACE).text
            vlan_state = vlan.find(".//ipi-vlan:customer-vlan/ipi-vlan:config/ipi-vlan:state", namespaces=NAMESPACE)

            if vlan_identifier == vlan_id and vlan_state is not None:
                is_l2_vlan = True

        return render_template("configure_interface.html", name=name, isL2Vlan=is_l2_vlan)

    if request.method == "POST":
        interface_name = request.form.get("interface-name")
        interface_ip = request.form.get("interface-ip")

        switchport_mode = request.form.get("switchport-mode")
        bind_interface_name = request.form.get("parent-interface")
        bind_bridge_id = request.form.get("bridge-interface")

        is_l2_vlan = request.form.get("is-l2-vlan")
        is_switchport = request.form.get("is-switchport")

        BIND_CONFIG = BIND_INTERFACE_TO_BRIDGE_CONFIG if bind_bridge_id is not None else BIND_L2_VLAN_TO_INTERFACE if is_l2_vlan == "True" and bind_interface_name is not None else BIND_L3_VLAN_TO_INTERFACE

        config_tree = ET.fromstring(INTERFACE_CONFIG)
        bind_config_tree = ET.fromstring(BIND_CONFIG)

        new_bind_config_tree = ""

        # Interface config xml parsing

        interface_element = config_tree.find(".//ipi-interface:interface", namespaces=NAMESPACE)
        ipv4_element = config_tree.find(".//ipi-if-ip:ipv4", namespaces=NAMESPACE)

        interface_name_tag = config_tree.find(".//ipi-interface:interface/ipi-interface:name", namespaces=NAMESPACE)
        interface_config_name_tag = config_tree.find(".//ipi-interface:interface/ipi-interface:config/ipi-interface:name", namespaces=NAMESPACE)
        interface_config_tag = config_tree.find(".//ipi-interface:interface/ipi-interface:config", namespaces=NAMESPACE)
        config_ip_tag = config_tree.find(".//ipi-if-ip:ipv4/ipi-if-ip:config/ipi-if-ip:primary-ip-addr", namespaces=NAMESPACE)

        if config_ip_tag is not None: config_ip_tag.text = interface_ip
        if interface_name_tag is not None: interface_name_tag.text = interface_name
        if interface_config_name_tag is not None: interface_config_name_tag.text = interface_name

        if interface_config_tag is not None and is_switchport:
            switchport_element = ET.Element("{http://www.ipinfusion.com/yang/ocnos/ipi-interface}enable-switchport")
            interface_config_tag.append(switchport_element)

        if is_switchport and interface_element is not None and ipv4_element is not None:
            interface_element.remove(ipv4_element)

        # Bind config xml parsing
        if bind_bridge_id is not None:
            bridge_id = bind_config_tree.find(".//ipi-network-instance:network-instance/ipi-network-instance:instance-name", namespaces=NAMESPACE)
            bridge_config_id = bind_config_tree.find(".//ipi-network-instance:network-instance/ipi-network-instance:config/ipi-network-instance:instance-name", namespaces=NAMESPACE)
            bridge_port_interface_name = bind_config_tree.find(".//ipi-bridge:bridge-ports/ipi-bridge:interface/ipi-bridge:name", namespaces=NAMESPACE)
            bridge_port_config_interface_name = bind_config_tree.find(".//ipi-bridge:bridge-ports/ipi-bridge:interface/ipi-bridge:config/ipi-bridge:name", namespaces=NAMESPACE)

            bridge_id.text = bind_bridge_id
            bridge_config_id.text = bind_bridge_id
            bridge_port_interface_name.text = interface_name
            bridge_port_config_interface_name.text = interface_name

            new_bind_config_tree = ET.tostring(bind_config_tree, encoding="unicode")

        if is_l2_vlan == "True" and bind_interface_name is not None:
            bind_interface_name_tag = bind_config_tree.find(".//ipi-interface:interface/ipi-interface:name", namespaces=NAMESPACE)
            bind_interface_config_name_tag = bind_config_tree.find(".//ipi-interface:interface/ipi-interface:config/ipi-interface:name", namespaces=NAMESPACE)
            bind_interface_mode_tag = bind_config_tree.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:interface-mode", namespaces=NAMESPACE)
            bind_interface_mode_config_tag = bind_config_tree.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:config/ipi-port-vlan:interface-mode", namespaces=NAMESPACE)
            bind_interface_vlan_id_tag = bind_config_tree.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:vlans/ipi-port-vlan:config/ipi-port-vlan:vlan-id", namespaces=NAMESPACE)

            bind_interface_name_tag.text = bind_interface_name
            bind_interface_config_name_tag.text = bind_interface_name
            bind_interface_mode_tag.text = switchport_mode
            bind_interface_mode_config_tag.text = switchport_mode
            bind_interface_vlan_id_tag.text = interface_name.split(".")[-1]

            new_bind_config_tree = ET.tostring(bind_config_tree, encoding="unicode")

        if is_l2_vlan == "False" and bind_interface_name is not None:
            bind_l3_interface_name_tag = bind_config_tree.find(".//ipi-interface:interface/ipi-interface:name", namespaces=NAMESPACE)
            bind_l3_interface_config_name_tag = bind_config_tree.find(".//ipi-interface:interface/ipi-interface:config/ipi-interface:name", namespaces=NAMESPACE)
            bind_l3_interface_mode_tag = bind_config_tree.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:interface-mode", namespaces=NAMESPACE)
            bind_l3_interface_mode_config_tag = bind_config_tree.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:config/ipi-port-vlan:interface-mode", namespaces=NAMESPACE)
            bind_l3_interface_vlan_id_tag = bind_config_tree.find(".//ipi-port-vlan:switched-vlans/ipi-port-vlan:switched-vlan/ipi-port-vlan:allowed-vlan/ipi-port-vlan:config/ipi-port-vlan:allowed-vlan-id", namespaces=NAMESPACE)

            bind_l3_interface_name_tag.text = bind_interface_name
            bind_l3_interface_config_name_tag.text = bind_interface_name
            bind_l3_interface_mode_tag.text = switchport_mode
            bind_l3_interface_mode_config_tag.text = switchport_mode
            bind_l3_interface_vlan_id_tag.text = interface_name.split(".")[-1]

            new_bind_config_tree = ET.tostring(bind_config_tree, encoding="unicode")

        new_config_tree = ET.tostring(config_tree, encoding="unicode")

        with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
            if bind_bridge_id is not None and bind_bridge_id != "":
                try:
                    result = m.edit_config(target="candidate", config=new_config_tree)
                    m.commit()

                    if "<ok/>" in str(result):
                        bind_bridge_result = m.edit_config(target="candidate", config=new_bind_config_tree)
                        m.commit()

                except Exception as e:
                    print(f"Error: {e}")
                    return redirect("/vlans/create-vlan")

            if bind_bridge_id is not None and bind_bridge_id == "":
                try:
                    print(new_config_tree)
                    result = m.edit_config(target="candidate", config=new_config_tree)
                    m.commit()

                except Exception as e:
                    print(f"Error: {e}")
                    return redirect("/vlans/create-vlan")

            if is_l2_vlan and bind_interface_name is not None:
                try:
                    bind_l2_vlan_result = m.edit_config(target="candidate", config=new_bind_config_tree)
                    m.commit()
                except Exception as e:
                    print(f"Error: {e}")
                    return redirect("/vlans/create-vlan")

            if not is_l2_vlan and bind_interface_name is not None:
                try:
                    result = m.edit_config(target="candidate", config=new_config_tree)
                    m.commit()

                    if "<ok/>" in str(result):
                        bind_l3_vlan_result = m.edit_config(target="candidate", config=new_bind_config_tree)
                        m.commit()
                except Exception as e:
                    print(f"Error: {e}")
                    return redirect("/vlans/create-vlan")
            
            return redirect("/interfaces/")
