# Mass-Queries
This repository contains the python script and associated YAML files for running queries across all organizations that you have access to.  It will return the results in a file called results.csv which is overwritten on each execution. This script is very useful from running security checks across the customers when a new exploit is discovered in the wild.

# Requirements

  * Python3
  * Properly formated YAML file
  * JWT from an authorized user

## Sample Execution

Create an environmental variable containing your JWT:

```
export JWT="Token 2222222-2222222-2222222-2222222"
```
Execute the python script with the appropriately formatted YAML file:
```
python3 mass_query.py -i queries.yaml
```
Sample Output:
```
Total Enterprise Devices
No Endpoint Security
No Configuration/Patch Management
EOL Operating Systems
EOL Systems without Endpoint Protection
Shadow IT - Virtual environments
```
## YAML Format
```
queries:
- name : 'Total Enterprise Devices'
  query : '{"combinator":"and","rules":[{"entity_type":"device","field":"asset_classification.category","operator":"equals","value":"EnterpriseEndpoint","valid":true,"scope":"ALL"}]}'
  source : ''
- name : 'No Endpoint Security'
  query : '{"combinator":"and","rules":[{"entity_type":"device","field":"asset_classification.category","operator":"equals","value":"EnterpriseEndpoint"},{"entity_type":"device","field":"controls","operator":"not_equals","value":"endpoint_security"},{"entity_type":"device","field":"last_activity_timestamp","operator":"greater","value":{"label":"7 days ago","raw":"now-7d/d"}},{"entity_type":"device","field":"tag_name","operator":"not_equals","value":{"name":"Exclude","value":"EPP"}}]}'
  source : ''
```
This script will loop through all the organizations that you have access to and run the queries you have in the YAML file.  The output will be in the same directory where the script is executed and named results.csv.  The format will be the query name as the header and then a row for each customer with the number of systems returned by that query.
