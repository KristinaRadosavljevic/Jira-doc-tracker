# Jira Documentation Tracker
Python application for collecting data relevant to the documentation process from Jira

## Table of Contents

## Introduction
The Jira Documentation Tracker is an application primarily intended for technical writers 
and developers in charge of writing documentation who use Jira for project management. It is 
intended as a tool to help them keep track of which Jira issues should be and have been 
documented.
### Assumptions
There are some general assumptions about the documentation process which this project heavily 
relies on:
- The Jira instance has been customized to include the following fields:
  - **Documentation**: A radio buttons field with values 'Yes' and 'No' which indicates whether 
  the issue should be documented.
  - **Docs**: A list where the user selects the document(s) which the Jira issue should affect.
  - **Done docs**: A list where the user selects the document(s) which have been updated.
- Excel is used to keep track of the documentation process. There are two workbooks for 
different aspects of this purpose:
  - **Documentation**: Used for listing the Jira issues which have already been tagged for 
  documentation (where **Documentation** has been set to **Yes**). In this workbook, the user 
  keeps track of which documents should be updated and which have already been modified and are 
  ready for review and publishing.
  - **Tickets**: Used for listing the Jira issues which have not been tagged for documentation
  (where **Documentation** has been set to **No**). In this workbook, the user can note down 
  any issues they think might affect some document(s) in order to ensure that nothing is missing 
  from documentation. Updating this workbook is currently not encompassed by this application 
  and the user is expected to maintain it mostly manually.
- In both Excel workbooks, the first row is a header with column names, and the issues are 
separated by a row consisting of merged cells according to which release they belong to. The 
release number is displayed in the merged row and new releases are always added at the top of 
the table.
- In both Excel workbooks, there are different tabs representing different development teams 
whose documentation process the user is in charge of tracking. These teams are tracked from 
Jira using the dedicated filters.
- In the **Documentation** workbook, there are the following columns (in order):
  - **Doc**: The number (code or name) of the document(s) which should be updated.
  - **Updated**: Whether the document(s) in the previous column have been updated.
  - **Assignee**: The developer assigned to the Jira issue, that is, the person who should 
  update the documentation.
  - **Jira ticket**: A unique Jira issue number.
  - **Description**: A short description of the issue, copied from the **Summary** field in 
  Jira.
  - **Status**: The status of the Jira issue (for example, **Done** or **In Progress**).
  - **Other columns**: There might be other columns which do not depend on Jira but are manually 
  filled in by the technical writer (such as whether the document(s) have been reviewed and 
  published, a place for additional comments, and so on).
### Aim of the project
There are two main problem areas that the Jira Documentation Tracker application aims to solve.
#### Jira to Excel copying
Due to the highly customized nature of the Jira instance used for keeping track of documentation, 
the information about the Jira issues which should affect documentation has to be manually 
copied from Jira and then pasted into the Excel sheet. This process is low-effort and very 
time-consuming.

Jira Documentation Tracker automates this process completely, saving time and eliminating error.
#### Tracking untagged issues
Generally, a development project will have a lot more Jira issues which should not be tagged to 
affect any document than the ones which should. Depending on the number of teams a technical 
writer is in charge of tracking and the number of issues created by each team, keeping track of 
all the untagged issues and periodically reviewing them can become impossible to do easily and 
accurately.

Jira Documentation Tracker helps make this task faster by providing a ready-made list of only 
those issues that the user has not reviewed. It also goes towards ensuring that no issue is 
left unreviewed.

## Functionalities

## Technologies
The following is a list of the most prominently used technologies and libraries in the project, 
along which their version:
- Python 3.7
- Jira REST API 3
- openpyxl 3.0.7
- SQLAlchemy 1.4.23
- alembic 1.7.1

For other technologies and associated libraries necessary for running the application, refer to 
the **requirements.txt** file.

## Launch

## Project status

###Useful alembic commands
Generate migration: `alembic revision --autogenerate -m "Example message"`

Upgrade to latest version: `alembic upgrade head`