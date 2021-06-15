import requests
from requests.auth import HTTPBasicAuth
import sqlite3
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

from config import username, password


def insert_headers(sheet, release, ticket_sheet=False):
    if sheet.merged_cells.ranges:
        sheet.merged_cells.ranges[0].shift(row_shift=1)
    sheet.insert_rows(2)
    if sheet.title == "Special":
        sheet.merge_cells('A2:J2')
    elif ticket_sheet:
        sheet.merge_cells('A2:G2')
    else:
        sheet.merge_cells('A2:I2')
    cell = sheet['A2']
    cell.value = release
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor="fff2cc")
    cell.alignment = Alignment(horizontal="center")
    sheet.insert_rows(3)


def api_request(url):
    auth = HTTPBasicAuth(username, password)
    headers = {
        "Accept": "application/json"
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )
    return response.json()


if __name__ == "__main__":

    # Inserting a header at the beginning of each sheet with the release number

    doc_file = "C:\\Users\\kiki\\OneDrive\\Documentation sheet.xlsx"
    issue_file = "C:\\Users\\kiki\\OneDrive\\Ticket sheet.xlsx"

    # doc_wb = openpyxl.load_workbook(doc_file)
    # for sheet in doc_wb:
    #     insert_headers(sheet, "Release 1")
    # doc_wb.save(doc_file)

    # issue_wb = openpyxl.load_workbook(issue_file)
    # for sheet in issue_wb:
    #     insert_headers(sheet, "Release 1", ticket_sheet=True)
    # issue_wb.save(issue_file)

    # Getting all issues in a filter

    url = 'https://jira-doc-tracker.atlassian.net/rest/api/3/filter/search?filterName="Team A R1"'
    query = api_request(url)
    teamA_filter = query['values'][0]['self']
    a_filter = api_request(teamA_filter)['jql']
    a_issues = api_request(f"https://jira-doc-tracker.atlassian.net/rest/api/3/search?jql={a_filter}")
    print(json.dumps(a_issues, sort_keys=True, indent=4))
    # print(json.dumps(data, sort_keys=True, indent=4)) I'm keeping this for the formatting
