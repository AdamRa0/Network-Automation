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
### Playing With OcNOS router

Contains two python files that fetch YANG schemas and NETCONF capabilities supported by my router.
It also fetches the running configuration of my router.

Add your router's IP, username and password as OS_ENV_VARIABLES

Run the python files and explore your router's capabilities and YANG schemas.

### Fetch Interface information
Fetches the name, operational status and admin status of interfaces created in the router

First, install all the required libraries in your python virtualenv. Then, set the IP_ADDR, USERNAME and PASSWORD for your OcNOS router as OS_ENV_VARIABLES.
```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

EXPORT IPADDR=< your OcNOS router IP >
EXPORT USERNAME=< your OcNOS router USERNAME >
EXPORT PASSWORD=< your OcNOS router PASSWORD>
```
Finally, run the file
```bash
python interfaces/fetch_interfaces_info.py
```

### Small Web App
Flask application that allows user to view relevant interface information and create new interface

#### Running the application
##### Via Docker
```bash
# Move into the interfaces/small_web_app folder and run
docker build . -t <desired tag>

# Run image
docker run <image-tag>

# Visit localhost:5000 in browser
```

##### No Docker
```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

```
Finally, run the file
```bash
python interfaces/fetch_interfaces_info.py
```