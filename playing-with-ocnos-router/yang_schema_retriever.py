import os
import ncclient
from ncclient import manager
import xml.etree.ElementTree as ET
import xml.dom.minidom

class YANGSchemaRetriever:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.connection = None
        self.schemas_dir = "yang_schemas"

    def connect(self):
        try:
            self.connection = manager.connect(
                host=self.host,
                username=self.username,
                password=self.password,
                hostkey_verify=False,
            )
            print("NetConf connection established successfully!")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def list_available_schemas(self):
        if not self.connection:
            print("Not connected. Please call .connect() first.")
            return []

        try:
            schemas_filter = '''
            <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                <netconf-state xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring">
                    <schemas/>
                </netconf-state>
            </filter>
            '''
            
            schemas_reply = self.connection.get(filter=schemas_filter)
            
            root = ET.fromstring(schemas_reply.xml)
            
            ns = {'netconf': 'urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring'}
            
            available_schemas = []
            for schema in root.findall('.//netconf:schema', namespaces=ns):
                schema_identifier = schema.find('netconf:identifier', namespaces=ns)
                schema_version = schema.find('netconf:version', namespaces=ns)
                schema_format = schema.find('netconf:format', namespaces=ns)
                
                if schema_identifier is not None:
                    schema_info = {
                        'identifier': schema_identifier.text,
                        'version': schema_version.text if schema_version is not None else 'Unknown',
                        'format': schema_format.text if schema_format is not None else 'Unknown'
                    }
                    available_schemas.append(schema_info)
            
            return available_schemas
        except Exception as e:
            print(f"Error retrieving schemas: {e}")
            return []

    def retrieve_schema(self, schema_identifier):
        if not self.connection:
            print("Not connected. Please call .connect() first.")
            return None

        try:
            os.makedirs(self.schemas_dir, exist_ok=True)
            
            schema = self.connection.get_schema(schema_identifier)
            
            safe_filename = "".join(x for x in schema_identifier if x.isalnum() or x in ".-_").rstrip()
            file_path = os.path.join(self.schemas_dir, f"{safe_filename}.yang")
            
            with open(file_path, 'w') as f:
                f.write(schema.data)
            
            print(f"Schema {schema_identifier} retrieved and saved to {file_path}")
            return file_path
        except Exception as e:
            print(f"Error retrieving schema {schema_identifier}: {e}")
            return None

    def retrieve_all_schemas(self):
        schemas = self.list_available_schemas()
        retrieved_schemas = []

        print(f"\nDiscovered {len(schemas)} schemas. Beginning retrieval...")
        
        for schema in schemas:
            print(f"\nRetrieving schema: {schema['identifier']}")
            print(f"Version: {schema['version']}")
            print(f"Format: {schema['format']}")
            
            # Attempt to retrieve the schema
            schema_path = self.retrieve_schema(schema['identifier'])
            if schema_path:
                retrieved_schemas.append(schema_path)
        
        return retrieved_schemas

    def interactive_schema_retrieval(self):
        print("\n=== YANG Schema Retrieval Demo ===")
        
        if not self.connect():
            return

        while True:
            print("\nChoose an option:")
            print("1. List Available Schemas")
            print("2. Retrieve Specific Schema")
            print("3. Retrieve ALL Schemas")
            print("4. Exit")
            
            choice = input("Enter your choice (1-4): ")
            
            if choice == '1':
                schemas = self.list_available_schemas()
                print("\nAvailable Schemas:")
                for schema in schemas:
                    print(f"- {schema['identifier']} (Version: {schema['version']})")
            
            elif choice == '2':
                schema_id = input("Enter the schema identifier to retrieve: ")
                self.retrieve_schema(schema_id)
            
            elif choice == '3':
                self.retrieve_all_schemas()
            
            elif choice == '4':
                print("Exiting YANG Schema Retrieval Demo.")
                break
            
            else:
                print("Invalid choice. Please try again.")

def main():
    print("YANG Schema Retrieval Program")
    print("--------------------------------")

    host = os.getenv("IP_ADDR")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    retriever = YANGSchemaRetriever(
        host=host,
        username=username,
        password=password
    )
    
    retriever.interactive_schema_retrieval()

if __name__ == '__main__':
    main()