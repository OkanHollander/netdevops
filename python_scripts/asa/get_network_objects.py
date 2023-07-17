# Cisco ASA restful API to obtain all address objects
# with the requests library
import requests
from rich import print as rprint
import yaml
import json
import ipaddress

# suppres warning messages
requests.packages.urllib3.disable_warnings()

def convert_json_to_yaml(json_data):
    try:
        json_data = yaml.safe_load(json_data)
        host_data = json_data.get('host', {})
        host_kind = host_data.get('kind', '')
        host_value = host_data.get('value', '')

        if host_kind == 'IPv4FQDN':
            ip_address = host_value
            subnet = ''
        else:
            ip_network = ipaddress.ip_network(host_value, strict=False)
            ip_address = str(ip_network.network_address)
            subnet = get_subnet(host_value)

        yaml_data = {
            'name': json_data.get('name', ''),
            'host': {
                'kind': host_kind,
                'value': ip_address,
                'subnet': subnet
            }
        }
        return yaml_data

    except json.JSONDecodeError as error:
        print("Error decoding JSON data:", str(error))
    except Exception as error:
        print("Error converting JSON to YAML:", str(error))


def get_subnet(cidr_address):
    try:
        network = ipaddress.ip_network(cidr_address, strict=False)
        subnet = str(network.netmask)
        return subnet
    except ValueError as error:
        print("Error getting subnet for IP address:", str(error))

def main():
    limit = 100
    offset = 0
    total_records = 0
    ip_address = "10.123.10.220"

    base_url = f"https://{ip_address}:443/api/objects/networkobjects?limit={limit}&offset={offset}"
    headers = {"Authorization": "Basic YWRtaW46YWRtaW4=",
               "Accept": "application/json"}
    while True:
        response = requests.get(url=base_url,
                                headers=headers,
                                verify=False,
                                timeout=10)
        if response.status_code != 200:
            rprint(f"Error: {response.status_code}")
        else:
            data = json.loads(response.text)
            if response.status_code == 200:
                results = data["items"]
                num_records = len(results)

                address_objects = []
                duplicates = []

                # Load existing YAML data
                existing_data = {}
                try:
                    with open('host_vars/FG-01.yml', 'r') as infile:
                        existing_data = yaml.safe_load(infile)
                except FileNotFoundError:
                    pass
                
                existing_objects = existing_data.get('address_objects', [])

                for result in results:
                    raw_json_output = result
                    json_output = json.dumps(raw_json_output)  # Convert dictionary to JSON string
                    yaml_output = convert_json_to_yaml(json_output)
                    
                    if yaml_output in existing_objects:
                        duplicates.append(yaml_output)
                    elif yaml_output in address_objects:
                        duplicates.append(yaml_output)
                    else:
                        address_objects.append(yaml_output)

                # Update the existing YAML data with new address objects
                existing_objects.extend(address_objects)
                updated_data = {'address_objects': existing_objects}

                # Write output to file
                with open(f'host_vars/FG-01.yml', 'w') as outfile:
                    yaml.dump(updated_data, outfile, sort_keys=False, default_flow_style=False)
        
                # update pagination limits for next iteration
                total_records += num_records
                offset += limit

                # Check if there are more records to retrieve
                if num_records < limit or total_records == data["rangeInfo"]["total"]:
                    break
                # Update the base_url for the next iteration
                base_url = f"https://10.123.10.220/api/objects/networkobjects?limit={limit}&offset={offset}"

            else:
                print(f"{response.status_code}")

if __name__ == "__main__":
    main()
 