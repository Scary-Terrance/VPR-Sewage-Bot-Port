#!/usr/local/bin/python2.7

import csv
import requests
from bs4 import BeautifulSoup

url = "https://anrweb.vt.gov/DEC/WWInventory/SewageOverflows.aspx"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
}

try:
    response = requests.get(url, headers=headers, timeout=5)
    html = response.content
    soup = BeautifulSoup(html, "lxml")

    try:
        table1 = soup.find("table", attrs={"class": "dataList", "id": "body_GridViewPublicAlerts"})
        table2 = soup.find("table", attrs={"class": "dataList", "id": "body_GridViewSewageOverflowsUnOfficial"})
        table3 = soup.find("table", attrs={"class": "dataList", "id": "body_GridViewSewageOverflowsAuthorized"})
        table4 = soup.find("table", attrs={"class": "dataList", "id": "body_GridViewSewageOverflowsOther"})

        list_of_rows1 = []
        list_of_rows2 = []
        list_of_rows3 = []
        list_of_rows4 = []
        final_list = []

        for row in table1.findAll("tr"):
            list_of_cells = []
            list_of_cells.append("Public Alert")
            for cell in row.findAll("td"):
                text = cell.text.replace("&nbsp;", "")
                list_of_cells.append(text)
            list_of_rows1.append(list_of_cells)
        del list_of_rows1[-1]

        for row in table2.findAll("tr"):
            list_of_cells = []
            list_of_cells.append("Pending Review")
            for cell in row.findAll("td"):
                text = cell.text.replace("&nbsp;", "")
                list_of_cells.append(text)
            list_of_rows2.append(list_of_cells)
        del list_of_rows2[-1]

        for row in table3.findAll("tr"):
            list_of_cells = []
            list_of_cells.append("Reviewed")
            for cell in row.findAll("td"):
                text = cell.text.replace("&nbsp;", "")
                list_of_cells.append(text)
            list_of_rows3.append(list_of_cells)
        del list_of_rows3[-1]

        for row in table4.findAll("tr"):
            list_of_cells = []
            list_of_cells.append("Reviewed")
            for cell in row.findAll("td"):
                text = cell.text.replace("&nbsp;", "")
                list_of_cells.append(text)
            list_of_rows4.append(list_of_cells)
        del list_of_rows4[-1]

        final_list = list_of_rows1 + list_of_rows2 + list_of_rows3 + list_of_rows4

        while [] in final_list:
            final_list.remove([])
            final_list.sort()

        outfile = open("data/sewage.csv", "w")
        writer = csv.writer(outfile)
        writer.writerow(["Status", "Index", "Start Date", "End Date", "Start/End Times", "Municipality", "Location", "Waterbody", "Description of Incident", "Estimated Volume (gallons)", "Wastewater Treatment Facility", "Contact Person"])
        list = writer.writerows(final_list)

        print("Scraping Complete")

    except AttributeError as e:
        print("Error accessing State Database: ", str(e))

except requests.exceptions.RequestException as e:
    print("Error loading web page: ", str(e))
