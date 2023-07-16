# Cisco ASA restful API to obtain all address objects
# with the requests library
import requests
from rich import print as rprint
import json

# suppres warning messages
requests.packages.urllib3.disable_warnings()

def main():
    limit = 100
    offset = 0
    total_records = 0

    base_url = f"https://10.123.10.220:443/api/objects/networkobjects?limit={limit}&offset={offset}"
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

                for result in results:
                    raw_output = result
                
                    #write output to file
                    with open('asa_output.json', 'a') as outfile:
                        json.dump(raw_output, outfile)
                    

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
