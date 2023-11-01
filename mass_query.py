import yaml
import requests
import os
import sys
import json
import ast
import argparse
import csv
import ast

def get_orgs():
    # Grab a list of orgs
    r = requests.get(api_endpoint+"/v1/admin/org",headers={ 'Authorization': token, 'X-Sevco-Target-Org': astk})
    r.raise_for_status()
    return(r.json())

def get_device_count_v3(org_id,path,query):
    # Build query structure
    payload = {
        "pagination": {},
        "query": query
    }
    headers = {
        "x-sevco-target-org": org_id,
        "authorization": token,
        "content-type": "application/json"
    }
    
    resp = requests.post(api_endpoint + path,headers=headers,json=payload)
    resp.raise_for_status()
    results = resp.json()
    return(results['pagination']['total'])

devices_path_v3 = "/v3/asset/device"
parser = argparse.ArgumentParser()
parser.add_argument("-i", required=True, dest="yamlfile", action="store",
                    help="YAML file containing customer configuration")

args = parser.parse_args()

# Load the variables from the YAML file
with open(args.yamlfile) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    sources = yaml.load(file, Loader=yaml.FullLoader)
    queries = sources['queries']

api_endpoint = "https://api.sev.co"
astk = "*"
org_dict = {}

# Check for API key to hit target ORG
if not os.environ.get("JWT"):
    raise Exception("Need API key in JWT environment variable.")
if os.environ.get("API"):
    api_endpoint = os.environ['API']

# Populate API creds
token = os.environ['JWT']

##############
csvfile=open('results.csv','w', newline='')
results=csv.writer(csvfile)
results_header = ['Org_Name','Org_ID']
#Populate the header file with query files from the YAML file
for query_name in queries:
    results_header.append(query_name)
#Write the header file
results.writerow(results_header)
#Get all the current orgs
orgs = get_orgs()

#Loop through all the orgs and run queries in yaml file
for org in orgs['orgs']:
    src_row = []
    src_row.append(org['org_name'])
    src_row.append(org['id'])
    #for loop for queries on each org
    for query_name in queries:
        print(query_name)
        q = json.loads(queries[query_name])
        src_row.append(get_device_count_v3(org['id'],devices_path_v3,q))
    results.writerow(src_row)
