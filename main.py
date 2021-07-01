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


def add_to_doc_sheet(issue, sheet, row):
    # Document numbers and done documentation
    if issue['fields']['customfield_10029']:
        docs = ""
        done = ""
        for doc in issue['fields']['customfield_10029']:
            if docs:
                docs += f", {doc}"
                if issue['fields']['customfield_10031'] and doc in issue['fields']['customfield_10031']:
                    done += ", Yes"
                else:
                    done += ", No"
            else:
                docs = doc
                if issue['fields']['customfield_10031'] and doc in issue['fields']['customfield_10031']:
                    done = "Yes"
                else:
                    done = "No"
        sheet[f'A{row}'].value = docs
        sheet[f'B{row}'].value = done
    else:
        sheet[f'A{row}'].value = "-"
        sheet[f'B{row}'].value = "-"
    # Assignee
    if issue['fields']['assignee']:
        sheet[f'C{row}'].value = issue['fields']['assignee']['displayName']
    else:
        sheet[f'C{row}'].value = "-"
    # Jira ticket number
    sheet[f'D{row}'].value = issue['key']
    # Summary/description
    sheet[f'E{row}'].value = issue['fields']['summary']
    # Status of the ticket
    sheet[f'F{row}'].value = issue['fields']['status']['name']


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

    doc_wb = openpyxl.load_workbook(doc_file)
    sheet_A = doc_wb['Team A']
    # for sheet in doc_wb:
    #     insert_headers(sheet, "Release 1")
    # doc_wb.save(doc_file)

    issue_wb = openpyxl.load_workbook(issue_file)
    # for sheet in issue_wb:
    #     insert_headers(sheet, "Release 1", ticket_sheet=True)
    # issue_wb.save(issue_file)

    # Getting all issues in a filter

    query_A = api_request('https://jira-doc-tracker.atlassian.net/rest/api/3/filter/search?filterName="Team A R1"')
    filter_A = query_A['values'][0]['self']
    jql_A = api_request(filter_A)['jql']
    issues_A = api_request(f"https://jira-doc-tracker.atlassian.net/rest/api/3/search?jql={jql_A}")
    print(json.dumps(issues_A, sort_keys=True, indent=4))

    # Inserting all documentation issues in a sheet

    # for issue in issues_A['issues']:
    #     if issue['fields']['customfield_10030'][0]['value'] == "Yes":
    #         sheet_A.insert_rows(3)
    #         add_to_doc_sheet(issue, sheet_A, 3)

    doc_wb.save(doc_file)
    # print(json.dumps(data, sort_keys=True, indent=4)) I'm keeping this for the formatting
