from flask import Flask, jsonify, render_template, request, redirect, Blueprint
from ncclient import manager
import xml.etree.ElementTree as ET


interface_bp = Blueprint("interfaces", __name__, url_prefix="/interfaces")
ns = {
  "ipi-interface": "http://www.ipinfusion.com/yang/ocnos/ipi-interface",
  "ipi-if-ip": "http://www.ipinfusion.com/yang/ocnos/ipi-if-ip"
}


@interface_bp.route("/")
def list_interfaces():
    netconf_filter = """
    <filter type="xpath">/ipi-interface:interfaces/ipi-interface:interface</filter>
    """

    with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
        result = m.get(filter=netconf_filter)

    tree = ET.fromstring(result.xml)

    interfaces = tree.findall(".//ipi-interface:interface", namespaces=ns)

    all_interfaces: list[dict[str, str]] = []

    for interface in interfaces:
        name = interface.find(".//ipi-interface:name", namespaces=ns).text
        oper_status = interface.find(".//ipi-interface:state/ipi-interface:oper-status", namespaces=ns).text
        admin_status = interface.find(".//ipi-interface:state/ipi-interface:admin-status", namespaces=ns).text

        all_interfaces.append({
            "name": name,
            "oper-status": oper_status,
            "admin-status": admin_status
        })

    return render_template('index.html', data=all_interfaces)

@interface_bp.route("/config-interface", methods=["POST"])
@interface_bp.route("/config-interface/<name>", methods=["GET"])
def configure_interface(name=None):

    if request.method == "GET":
        return render_template("configure_interface.html", name=name)

    if request.method == "POST":
        interface_name = request.form.get("interface-name")
        interface_ip = request.form.get("interface-ip")

        CONFIGURE_INTERFACE_CONFIG = f"""
        <config>
          <interfaces xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface">
            <interface>
              <name>{interface_name}</name>
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

        config_tree = ET.fromstring(CONFIGURE_INTERFACE_CONFIG)

        config_name_tag = config_tree.find(".//ipi-interface:config/ipi-interface:name", namespaces=ns)
        config_ip_tag = config_tree.find(".//ipi-if-ip:ipv4/ipi-if-ip:config/ipi-if-ip:primary-ip-addr", namespaces=ns)

        if config_name_tag is not None: config_name_tag.text = interface_name
        if config_ip_tag is not None: config_ip_tag.text = interface_ip

        new_config_tree = ET.tostring(config_tree, encoding="unicode")

        with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
            result = m.edit_config(target="candidate", config=new_config_tree)
            m.commit()

        if "<ok/>" in str(result):
            return redirect("/")
        else:
            print("failed to execute " % CONFIGURE_INTERFACE_CONFIG)
