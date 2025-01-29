from flask import Flask, jsonify, render_template, request, redirect
from ncclient import manager
import xml.etree.ElementTree as ET


app = Flask(__name__)
ns = {"ipi-interface": "http://www.ipinfusion.com/yang/ocnos/ipi-interface"}


@app.route("/")
def list_interfaces():
    netconf_filter = """
    <filter type="xpath">/ipi-interface:interfaces/ipi-interface:interface</filter>
    """

    # Don't expose your public IP and creds like this. Store in config file. Preferably in instance folder
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


@app.route("/new-interface", methods=["GET", "POST"])
def create_interface():
    CREATE_INTERFACE_CONFIG = """
     <config>
      <interfaces xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-interface">
        <interface>
          <name></name>
          <config>
            <name></name>
            <vrf-name>default</vrf-name>
          </config>
          <ipv4 xmlns="http://www.ipinfusion.com/yang/ocnos/ipi-if-ip">
            <config>
              <enable-dhcp-ip-address></enable-dhcp-ip-address>
            </config>
          </ipv4>
        </interface>
      </interfaces>
    </config>
    """

    if request.method == "GET":
        return render_template("create_interface.html")

    if request.method == "POST":
        interface_name = request.form.get("interface-name")

        config_tree = ET.fromstring(CREATE_INTERFACE_CONFIG)

        name_tag = config_tree.find(".//ipi-interface:name", namespaces=ns)
        config_name_tag = config_tree.find(".//ipi-interface:config/ipi-interface:name", namespaces=ns)

        if name_tag is not None: name_tag.text = interface_name
        if config_name_tag is not None: config_name_tag.text = interface_name

        new_config_tree = ET.tostring(config_tree, encoding="unicode")

        # Don't expose your public IP and creds like this. Store in config file. Preferably in instance folder
        with manager.connect(host="192.168.10.102", username="ocnos", password="ocnos", hostkey_verify=False) as m:
            result = m.edit_config(target="candidate", config=new_config_tree)
            m.commit()

        if "<ok/>" in str(result):
            return redirect("/")
        else:
            print("failed to execute " % CONFIG_INTERFACE)


if __name__ == "__main__":
    app.run(debug=True)