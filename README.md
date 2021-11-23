# Jira Documentation Tracker
Python application for collecting data relevant to the documentation process from Jira

## Table of Contents
- [Introduction](#introduction)
  - [Assumptions](#assumptions)
  - [Aim of the project](#aim-of-the-project)
- [Functionalities](#functionalities)
- [Technologies](#technologies)
- [Launch](#launch)
  - [Special considerations when running the application](#special-considerations-when-running-the-application)

## Introduction
Jira Documentation Tracker is an application primarily intended for technical writers 
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
Jira using the dedicated filters, whose names consist of the team name and the release number, 
separated by a single space.
- In the Documentation workbook, there are the following columns (in order):
  - **Doc**: The number (code or name) of the document(s) which should be updated.
  - **Updated**: Whether the document(s) in the previous column have been updated.
  - **Assignee**: The developer assigned to the Jira issue, that is, the person who should 
  update the documentation.
  - **Jira ticket**: A unique Jira issue number.
  - **Description**: A short description of the issue, copied from the **Summary** field in 
  Jira.
  - **Status**: The status of the Jira issue (for example, **Done** or **In Progress**).
  - **Other columns**: There are other columns which do not depend on Jira but are manually 
  filled in by the technical writer (such as whether the document(s) have been reviewed and 
  published, a place for additional comments, and so on).
- In the Documentation workbook, there is a 'special' sheet where all the issues affecting the 
'special' document are listed. The columns in this sheet differ from the ones in other sheets 
described in the previous point, and are as follows (in order):
  - **Jira ticket**: A unique Jira issue number.
  - **Description**: A short description of the issue, copied from the **Summary** field in 
  Jira.
  - **Status**: The status of the Jira issue (for example, **Done** or **In Progress**).
  - **Updated**: Whether the 'special' document has been updated.
  - **Scale**: How large the change to the document is, that is, how much time documenting it 
  is likely to take.
  - **Member**: The technical writer in charge of documenting the issue.
  - **Team**: The name of the development team to which the issue belongs.
  - **Assignee**: The developer assigned to the Jira issue, that is, the person who should 
  update the documentation.
  - **Other columns**: There are other columns which do not depend on Jira but are manually 
  filled in by the technical writer (such as which topic the 'special' document should affect, 
  a place for additional comments, and so on).
- There is a total of nine columns in each sheet of the Documentation workbook (except in the 
'Special' sheet, where there are ten) and a total of seven columns in each sheet of the Ticket 
workbook.
### Aim of the project
There are two main problem areas that the Jira Documentation Tracker application aims to solve.
#### Jira to Excel copying
Due to the highly customized nature of the Jira instance used for keeping track of documentation, 
the information about the Jira issues which should affect documentation has to be manually 
copied from Jira and then pasted into the Excel sheet. This process is low-effort but very 
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
The following are three main functionalities of Jira Documentation Tracker, all accessible from 
the initial view which is opened when the front-end application is run:
- **Add a New Project**: Store the current release number in the database so that it is always 
accessible until the next release number is specified. This functionality also adds release 
headers in both workbooks.
- **Update the Sheet**: Select a team and the application compares the data in the relevant 
sheet to the team's Jira issues, adds any newly found issues to the sheet, and highlights the 
rows with issues which are no longer found in the Jira filter. It is possible to update all 
sheets in the workbook at once.
- **Review Jira Issues**: For the selected team, you get a list of all untagged issues which you 
have not seen/reviewed, as well as the ones which you have decided should not be documented but 
have transitioned into status **Done** in the meantime.

## Technologies
The following is a list of the most prominently used technologies and libraries in the project, 
along with their version:
- Python 3.7
- Jira REST API 3
- openpyxl 3.0.7
- SQLAlchemy 1.4.23
- alembic 1.7.1

For other technologies and associated libraries necessary for running the application, refer to 
the **requirements.txt** file.

## Launch
Before launching the application, perform the following steps (the recommended development 
environment is PyCharm):
1. Enter the following command in the terminal to install all the required packages: 
`pip install -r requirements.txt`.
2. Make a Python file in the main directory called **config.py**, which contains two variables:
    - **username**: Assigned to the username for the basic authentication for Jira, in string 
   format.
    - **password**: Assigned to the corresponding password for Jira authentication, in string 
   format.
3. Edit the path to the Excel files containing Documentation and Ticket workbooks in the 
**doc_file** and **issue_file** variables respectively (lines 12 and 13 in **main.py**).
4. Edit the name of the 'Special' sheet (lines 67 and 169 in **main.py**).
5. Edit the code of the 'special' document by modifying all occurrences of `"01"` in **main.py**.
6. Edit the names of the following custom fields in Jira to correspond to your Jira instance:
    - **customfield_10029**: The reference to the **Docs** field (all occurrences in **main.py**).
    - **customfield_10031**: The reference to the **Done Docs** field (all occurrences in 
   **main.py**).
    - **Documentation[Checkboxes]**: The reference to the **Documentation** field in the JQL 
   (line 254 in **main.py**).
7. Edit the team names in the list assigned to the **teams** variable (lines 85 and 156 in 
**front.py**). The team names must be exactly the same as the titles of the tabs in the 
Documentation workbook.
8. Edit the URL to your Jira instance (line 290 in **front.py**).
9. Upgrade the database to the latest migration by entering the following line in the terminal: 
`alembic upgrade head`. (If you make changes to the database structure, generate a new 
migration by entering `alembic revision --autogenerate -m "Example message"` and upgrade to 
that migration again.)

The Jira Documentation Tracker front-end application is opened by running the **front.py** file.
### Special considerations when running the application
- You must be logged into Jira on the machine from which you run the application.
- Make sure that the Excel files are closed when the application is modifying them, otherwise 
the files will be saved under a different name in the same directory instead of being overridden.