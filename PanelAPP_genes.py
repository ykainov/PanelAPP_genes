import requests
import json
import pandas as pd
import sys

def get_gene_information():

    server = "https://panelapp.genomicsengland.co.uk"
    ext = f"/api/v1/genes/"

    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    expected_genes = r.json()["count"]

    gene_df = pd.json_normalize(r.json(), record_path=["results"])

    while r.json()["next"] is not None:
        r = requests.get(r.json()["next"], headers={"Content-Type": "application/json"})
        data = pd.json_normalize(r.json(), record_path=["results"])
        gene_df = pd.concat([gene_df, data], ignore_index=True)

    return gene_df

# Call the function to get gene information
gene_information_df = get_gene_information()

# Save the gene information dataframe to a CSV file without column names
gene_information_df.to_csv("PanelApp_genes.csv", index=False)

