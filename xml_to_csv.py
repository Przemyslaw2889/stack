#!/usr/bin/env python

import xml.etree.cElementTree as et
import os
import pandas as pd


def save_xml_as_csv(dataset_name):
    """Saves all tables of dataset as csv's"""
    data_path = os.path.join("data", dataset_name + ".stackexchange.com")
    if not os.path.exists(data_path):
        print("Check whether path {} exists!".format(data_path))

    for table_name in os.listdir(data_path):
        table_path = os.path.join(data_path, table_name)

        if table_path.endswith('xml'):
            # Parsing XML
            parsedXML = et.parse(table_path)
            root = parsedXML.getroot()

            # Saving data frame as a csv
            df = pd.DataFrame([row.attrib for row in root])
            save_path = os.path.splitext(table_path)[0] + ".csv"
            df.to_csv(save_path)
            print("Saved {} from {}".format(table_name, dataset_name))


def main():
    """ Napisz w argumencie jaki zbiór chcesz przerobić na csv
    Dane musza byc wypakowane w folderze data.
    Pliki .csv zapisuja sie w folderze gdzie znajduja sie pliki .xml
    Moze sie troche mielic."""
    
    save_xml_as_csv("movies")
    save_xml_as_csv("writers")


if __name__ == "__main__":
    main()
