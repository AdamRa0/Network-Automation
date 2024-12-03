from ncclient import manager

with manager.connect(host="192.168.5.1", username="admin", password="@adm1n", hostkey_verify=False) as m:
    filter = """
    <system xmlns="urn:github.com/AdamRa0/Network-Automation">
        <hostname/>
    </system>
    """

    response = m.get(filter=filter)

    print(response.xml)