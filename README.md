# Network-Automation
Learning YANG, NETCONF and Ansible.

## Running the project
- Pinging my router
>> You'll need your own router with private IP configured
>> Change IP in hosts file to that of your router
>> Run
>>> ```bash
>>> ansible router -m ping -v
>>> ```
>> Expected result
>>> ```bash
>>> <your router\'s IP> | SUCCESS => {
>>>    "ansible_facts": {
>>>        "discovered_interpreter_python": "/usr/bin/python3.12"
>>>    },
>>>    "changed": false,
>>>    "ping": "pong"
>>>}
>>> ```
- Playing With OcNOS router

Contains two python files that fetch YANG schemas and NETCONF capabilities supported by my router.
It also fetches the running configuration of my router.

Add your router's IP, username and password as OS_ENV_VARIABLES

Run the python files and explore your router's capabilities and YANG schemas.