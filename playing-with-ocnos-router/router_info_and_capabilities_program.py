import ncclient
from ncclient import manager
import xml.dom.minidom

class NetconfYangLearner:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = manager.connect(
                host=self.host,
                username=self.username,
                password=self.password,
                hostkey_verify=False,
            )
            print("NetConf connection established successfully!")
        except Exception as e:
            print(f"Connection error: {e}")

    def get_capabilities(self):
        if not self.connection:
            print("Please connect first using .connect() method")
            return

        for capability in self.connection.server_capabilities:
            print(capability)

    def get_running_config(self):
        if not self.connection:
            print("Please connect first using .connect() method")
            return

        try:
            netconf_reply = self.connection.get_config(source='running')
            
            xml_str = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
            print("\n--- Running Configuration ---")
            print(xml_str)
        except Exception as e:
            print(f"Error retrieving configuration: {e}")

    def interactive_demo(self):
        print("\n=== NetConf and YANG Learning Demo ===")
        print("1. Connect to Router")
        print("2. View Router Capabilities")
        print("3. Retrieve Running Configuration")
        print("4. Exit")

        while True:
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.connect()
            elif choice == '2':
                self.get_capabilities()
            elif choice == '3':
                self.get_running_config()
            elif choice == '4':
                self.explore_yang_models()
            elif choice == '5':
                print("Exiting NetConf Learning Demo.")
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    print("NetConf Learning Program")
    print("--------------------------------")
    
    host = os.getenv("IP_ADDR")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    demo = NetconfYangLearner(
        host=host,
        username=username,
        password=password
    )
    
    demo.interactive_demo()

if __name__ == '__main__':
    main()