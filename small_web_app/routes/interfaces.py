from flask import Flask, jsonify, render_template, request, redirect, Blueprint
from ncclient import manager
import xml.etree.ElementTree as ET

from constants import NAMESPACE
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
        vlan_id = name.split(".")[-1]

        is_l2_vlan = False

        netconf_filter = provide_filter_string("/ipi-network-instance:instances/ipi-network-instance:instance")

        with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
            result = m.get(filter=netconf_filter)

        tree = ET.fromstring(result.xml)

        vlans = tree.findall(".//ipi-vlan:vlan", namespaces=NAMESPACE)

        for vlan in vlans:
            vlan_identifier = vlan.find(".//ipi-vlan:vlan-id", namespaces=NAMESPACE).text
            vlan_state = vlan.find(".//ipi-vlan:customer-vlan/ipi-vlan:config/ipi-vlan:state")

            if vlan_identifier == vlan_id and vlan_state is not None:
                is_l2_vlan = True

        return render_template("configure_interface.html", name=name, isL2Vlan=is_l2_vlan)

    if request.method == "POST":
        interface_name = request.form.get("interface-name")
        interface_ip = request.form.get("interface-ip")

        CONFIGURE_INTERFACE_CONFIG = f"""
        <config>
          <interfaces xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface">
            <interface>
              <name>{interface_name}</name>
              <config>
                <name>{interface_name}</name>
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

        config_tree = ET.fromstring(CONFIGURE_INTERFACE_CONFIG)

        config_ip_tag = config_tree.find(".//ipi-if-ip:ipv4/ipi-if-ip:config/ipi-if-ip:primary-ip-addr", namespaces=NAMESPACE)

        if config_ip_tag is not None: config_ip_tag.text = interface_ip

        new_config_tree = ET.tostring(config_tree, encoding="unicode")

        with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
            result = m.edit_config(target="candidate", config=new_config_tree)
            m.commit()

        if "<ok/>" in str(result):
            return redirect("/interfaces/")
        else:
            print("failed to execute " % CONFIGURE_INTERFACE_CONFIG)
