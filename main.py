import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

from config import username, password


def insert_headers(sheet, release):
    sheet.merged_cells.ranges[0].shift(row_shift=1)
    sheet.insert_rows(2)
    if sheet.title == "Special":
        sheet.merge_cells('A2:J2')
    else:
        sheet.merge_cells('A2:I2')
    cell = sheet['A2']
    cell.value = release
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor="fff2cc")
    cell.alignment = Alignment(horizontal="center")
    sheet.insert_rows(3)


if __name__ == "__main__":
    # url = "https://jira-doc-tracker.atlassian.net/rest/api/3/issue/PC-1"
    # auth = HTTPBasicAuth(username, password)
    # headers = {
    #    "Accept": "application/json"
    # }
    # response = requests.request(
    #    "GET",
    #    url,
    #    headers=headers,
    #    auth=auth
    # )
    # data = response.json()
    # summary = data['fields']['summary']
    # print(summary)

    # Inserting a header at the beginning of each sheet with the release number
    file = "C:\\Users\\kiki\\OneDrive\\Documentation sheet.xlsx"
    workbook = openpyxl.load_workbook(file)
    for sheet in workbook:
        insert_headers(sheet, "Release 1")
    workbook.save(file)
