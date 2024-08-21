"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path='data/neos.csv'):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neos = []
    with open(neo_csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if reader.line_num > 10:  # Limit loading to 10 values!!!
                break
            # Print the row to see the data only for these 4 columns
            # print(f"pdes:'{row['pdes']}', name:'{row['name']}', diameter:'{row['diameter']}', pha:'{row['pha']}'")    
            neos.append(NearEarthObject(pdes=row['pdes'], name=row['name'], 
                                        diameter=row['diameter'], pha=row['pha']))
    return neos


def load_approaches(cad_json_path='data/cad.json'):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    approaches = []
    with open(cad_json_path) as f:
        data = json.load(f)
        for row in data['data']:
            if len(approaches) > 100:  # Limit loading to 10 values!!!
                break
            # Print the row to see the data only for these 3 columns
            # print(f"cd:'{row[3]}', dist:'{row[4]}', v_rel:'{row[7]}'")
            # "fields":["des", "orbit_id", "jd", "cd", "dist", "dist_min", "dist_max", "v_rel", "v_inf", "t_sigma_f", "h"]
            approaches.append(CloseApproach(des=row[0], cd=row[3], dist=row[4], v_rel=row[7]))
    return approaches