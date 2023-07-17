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
        ip_address = json_data.get('host', {}).get('value', '')
        subnet = get_subnet(ip_address)
        
        yaml_data = {
            'name': json_data.get('name', ''),
            'host': {
                'kind': json_data.get('host', {}).get('kind', ''),
                'value': ip_address,
                'subnet': subnet
            }
        }
        return yaml_data

    except json.JSONDecodeError as error:
        print("Error decoding JSON data:", str(error))
    except Exception as error:
        print("Error converting JSON to YAML:", str(error))
        
def get_subnet(ip_address):
    try:
        network = ipaddress.ip_network(ip_address)
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

                for result in results:
                    raw_json_output = result
                    json_output = json.dumps(raw_json_output)  # Convert dictionary to JSON string
                    yaml_output = convert_json_to_yaml(json_output)
                    if yaml_output in address_objects:
                        duplicates.append(yaml_output)
                    else:
                        address_objects.append(yaml_output)
                
                yaml_data = yaml.dump({'address_objects' : address_objects},
                                      sort_keys=False,
                                      default_flow_style=False)
                    # Write output to file
                with open(f'host_vars/FG-01.yml', 'a') as outfile:
                    outfile.write(yaml_data)
                

                if duplicates:
                    rprint("Duplicate Entries:")
                for duplicate in duplicates:
                    rprint(duplicate)

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
 