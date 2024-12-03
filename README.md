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