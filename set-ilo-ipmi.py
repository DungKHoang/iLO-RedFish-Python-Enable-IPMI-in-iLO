# ---------------------------------------------------------------------------------------------------------------------------
# Copyright 2018 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import requests, json, sys, re, time, os, warnings, argparse, csv
from hpOneView.exceptions import HPOneViewException
from hpOneView.oneview_client import OneViewClient

TABSPACE        = "    "
COMMA           = ','
CR              = '\n'
CRLF            = '\r\n'


_home           = (os.environ['SYNERGY_AUTO_HOME'])
config_file     = _home + '/configFiles/oneview_config.json'


# Connect to new OneView instance 
print(CR)
print('#---------------- Connect to Oneview instance')

with open(config_file) as json_data:
    config = json.load(json_data)


oneview_client          = OneViewClient(config)
ov_headers              = oneview_client.connection._headers

# get all server hardware
server_hardware_all     = oneview_client.server_hardware.get_all()
# For a specific server, use this call
name                    = 'F3-CN75140CR6, bay 7'
server_hardware_all     = oneview_client.server_hardware.get_by('name', name) 


for server in server_hardware_all:
    mpIpAddresses       = server['mpHostInfo']['mpIpAddresses']
    for ipAdr in mpIpAddresses:
        if 'LinkLocal' != ipAdr['type']:
            iLOip       = ipAdr['address']



login_account           = 'administrator'
login_password          = 'password'
uri                     = "https://{0}/{1}".format(iLOip,'redfish/v1/Managers/1/NetworkService')
response                = requests.get(uri, verify=False,auth=(login_account,login_password))
data                    = response.json()


# Enable IPMI
headers                 = {'content-type': 'application/json'}

body                    = { "IPMI" : {"ProtocolEnabled": True} }



response                = requests.patch(uri, data= json.dumps(body), headers=headers,verify=False, auth=(login_account,login_password))

statusCode              = response.status_code

if statusCode           == 200:

    print("\n- PASS, status code %s returned for PATCH command, IPMI configured ") % statusCode

else:

    print("\n- FAIL, status code %s returned for PATCH command, IPMI not configured") % statusCode

    sys.exit()