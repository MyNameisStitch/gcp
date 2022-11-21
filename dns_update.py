#Import required python libraries.
#========================
import json
import requests
import time
import dns.resolver
#========================
#Pull currently assigned record for the specified hostname. 
curr_ip = dns.resolver.resolve('www.brewednhopd.net.', 'A')
curr_ip = curr_ip[0]
#========================
#Import Google Cloud Python Library after dns.resolver is completed to prevent name conflicts with “dns” functions.
from google.cloud import dns 
#Pull current VM public IP address. 
ext_ip = (json.loads(requests.get('https://ip.seeip.org/jsonip?').text)['ip'])
#========================
ttl = 5 * 60  #Create ttl for new DNS Record. This is 5 minutes.
#========================
#Input zone and record data.
cloud_dns = dns.Client(project='emerald-cumulus-369200')
zone = cloud_dns.zone('my-new-zone', 'brewdnhopd.net.')
#========================
# Remove Old Record
record1 = zone.resource_record_set('www.brewdnhopd.net.','A',ttl,[f"{curr_ip}"])
changes = zone.changes()
changes.delete_record_set(record1)
changes.create()
while changes.status != 'done':
    print(f'Record Deletion Status: {changes.status}')
    time.sleep(30)     # or whatever interval is appropriate
    changes.reload()   # API request
print(f'Record Deletion Status: {changes.status}')
#========================
# Create New Record
record = zone.resource_record_set('www.brewdnhopd.net.','A',ttl,[f"{ext_ip}"])
changes = zone.changes()
changes.add_record_set(record)
changes.create()
while changes.status != 'done':
    print(f'Record Update Status: {changes.status}')
    time.sleep(30)     # or whatever interval is appropriate
    changes.reload()   # API request
print(f'Record Update Status: {changes.status}')
