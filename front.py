# This file contains the frond-end functionality organized in classes.
# The Jira Tracker application and all its functionalities should be initiated by running this file.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser

import main
from utils import get_session
from db_models import IssuesInSheet, IgnoredIssues


class InitialView(ttk.Frame):
    """
    The first view the user sees when running the application.
    From here, it is possible to choose which action to run - adding a new project, updating sheets,
    or reviewing Jira issues not tagged to affect documentation.
    """

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Jira Documentation Tracker")
        ttk.Button(self, text="Add a New Project", command=self.add_project) \
            .grid(row=0, column=0, padx=20, pady=20)
        ttk.Button(self, text="Update the Sheet", command=self.update_sheets) \
            .grid(row=0, column=1, pady=20)
        ttk.Button(self, text="Review Jira Issues", command=self.review_issues) \
            .grid(row=0, column=2, padx=20, pady=20)

    def add_project(self):
        """
        Displays the Add a New Project view.
        """
        self.destroy()
        NewProject(self.parent).pack(side="top", fill="both", expand=True)

    def update_sheets(self):
        """
        Displays the Update the Sheet view.
        """
        self.destroy()
        UpdateSheets(self.parent).pack(side="top", fill="both", expand=True)

    def review_issues(self):
        """
        Displays the Review Jira Issues view.
        """
        self.destroy()
        JiraIssues(self.parent).pack(side="top", fill="both", expand=True)


class SecondaryView(ttk.Frame):
    """
    Abstract class used as a blueprint for the NewProject, UpdateSheets, and JiraIssues views.
    Only implements the Back button functionality.
    """

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.back_button = ttk.Button(self, text="Back", command=self.back)

    def back(self):
        """
        Displays the Initial View.
        """
        self.destroy()
        InitialView(self.parent).pack(side="top", fill="both", expand=True)

    def team_frame(self, label, command):
        """
        Creates a frame with a team names drop-down list and a button.

        Arguments:
            label (str) - The label for the button.
            command (func) - The function which should be bound to the button.
        """
        input_frame = ttk.Frame(self, relief="groove", width=350, height=100)
        input_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=10, ipady=10)
        ttk.Label(input_frame, text="Select a team:", justify="center") \
            .grid(row=0, column=0, padx=15, pady=5)
        team = tk.StringVar()
        teams = ("Team A", "Team B", "Team C")
        ttk.Combobox(input_frame, values=teams, state="readonly", textvariable=team) \
            .grid(row=1, column=0, padx=15, pady=5)
        team.set(teams[0])
        ttk.Button(input_frame, text=label, command=lambda: command(team.get())) \
            .grid(row=2, column=0, padx=15, pady=5)


class NewProject(SecondaryView):
    """
    The view in which the user can add the next release number to be used throughout the application.
    """

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Add a New Project")
        ttk.Label(self, text="Enter the release number:") \
            .grid(row=0, column=0, columnspan=5, padx=20, pady=10)
        self.entry = ttk.Entry(self, width=20)
        self.entry.grid(row=1, column=0, columnspan=5, padx=20, pady=10)
        ttk.Label(self,
                  text="Note: Make sure that all the filters for this project are set up in Jira"
                       " and that they are correctly named.",
                  wraplength=350, justify="center", foreground="grey") \
            .grid(row=2, column=0, columnspan=5, padx=20, pady=10)
        ttk.Button(self, text="Enter", command=self.apply) \
            .grid(row=3, column=1, padx=20, pady=10)
        self.back_button.grid(row=3, column=3, padx=20, pady=10)

    def apply(self):
        """
        Retrieves the value from the release number field, adds it to the database, and inserts the
        headers with the new release number into all sheets.
        """
        release = self.entry.get()
        main.add_release_to_db(release)
        main.insert_headers()
        messagebox.showinfo(title="Success", message="New project was added to the workbooks.")


class UpdateSheets(SecondaryView):
    """
    The view from which the user can update the issues in the Documentation workbook. This workbook
    only contains issues which are tagged to affect documentation.
    The user can choose to update the sheet for a particular team or to update all sheets at once.
    """

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Update the Sheet")
        self.team_frame("Update", self.update_sheet)
        ttk.Label(self, text="- or -", justify="center") \
            .grid(row=1, column=0, columnspan=2)
        ttk.Button(self, text="Update All Sheets", command=self.update_all) \
            .grid(row=2, column=0, columnspan=2, padx=20, pady=15)
        self.back_button.grid(row=3, column=1, padx=20, pady=10, sticky="e")

    def update_sheet(self, team):
        """
        Updates information about issues from the selected team in the relevant sheet.

        Arguments:
            team (str) - The name of the team whose sheet should be updated.
        """
        main.update_sheet(team)
        messagebox.showinfo(title="Success", message="The sheet was successfully updated.")

    def update_all(self):
        """
        Updates information about issues in all sheets in the Documentation workbook.
        """
        teams = ("Team A", "Team B", "Team C")
        for team in teams:
            main.update_sheet(team)
        messagebox.showinfo(title="Success", message="The sheets were successfully updated.")


class JiraIssues(SecondaryView):
    """
    The view in which the user can see all Jira issues which are not tagged to affect documentation
    from the selected team.
    There are two frames which display issues: New Issues and Done Issues.
    The New Issues frame shows new issues which the user has never reviewed before.
    The Done Issues frame shows issues which the user has previously ignored but have not transitioned
    into the Done status, giving the user an opportunity to review their previous decision.
    """

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Review Jira Issues")
        self.team_frame("Find Issues", self.find_issues)
        self.new_frame = IssuesFrame(self, "New", text="New Issues")
        self.new_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10, ipady=10, ipadx=10)
        self.done_frame = IssuesFrame(self, "Done", text="Done Issues")
        self.done_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=10, ipady=10, ipadx=10)
        self.back_button.grid(row=3, column=1, padx=20, pady=10, sticky="e")

    def find_issues(self, team):
        """
        Gets the list of Jira issues for the selected team which are not tagged to affect documentation
        and divides them into two lists based on whether they should be included in New Issues or
        Done Issues.

        Arguments:
            team (str) - The name of the team for which issues should be retrieved.
        """
        new_list = []
        done_list = []
        list_all = main.get_issues(f"{team} {main.current_release}", "No")
        for issue in list_all:
            issue_nbr = issue['key']
            session = get_session()
            in_ignored = session.query(IgnoredIssues).filter_by(id=issue_nbr).first()
            in_sheet = session.query(IssuesInSheet).filter_by(id=issue_nbr).first()
            if not in_sheet and not in_ignored:
                new_list.append(issue)
            elif in_ignored and in_ignored.status != "Done" and issue['fields']['status']['name'] == "Done":
                done_list.append(issue)
            session.close()
        self.new_frame.populate(new_list)
        self.done_frame.populate(done_list)


class IssuesFrame(ttk.LabelFrame):
    """
    The common class for both New Issues and Done Issues frames.
    Contains rows with Jira issues or a placeholder text if there are no more rows.
    """

    def __init__(self, parent, title, *args, **kwargs):
        ttk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.title = title
        self.placeholder = ttk.Label(self, text="Select a team and click 'Find Issues'.",
                                     foreground="grey")
        self.placeholder.pack()
        self.issues = []
        self.row = 3

    def populate(self, issue_list):
        """
        Adds all the retrieved Jira issues as rows to the frame.
        Only three rows are displayed at the time. The title of the frame is updated with information
        about the number of the remaining (undisplayed) issues.

        Arguments:
            issue_list (list) - The list of undisplayed issues for the relevant frame.
        """
        for item in self.winfo_children():
            item.destroy()
        if issue_list:
            row = 0
            for issue in issue_list:
                if row < 3:
                    IssueRow(self, issue['key'], issue['fields']['summary'], issue['fields']['status']['name']).pack()
                    row += 1
                else:
                    self.issues.append((issue['key'], issue['fields']['summary'], issue['fields']['status']['name']))
        if self.issues:
            self.config(text=f"{self.title} Issues ({len(self.issues)} more)")

    def display_issue(self):
        """
        Displays the next available undisplayed Jira issue (if any) when any of the already displayed
        ones are removed and updates the frame title accordingly.
        """
        if self.issues:
            IssueRow(self, self.issues[0][0], self.issues[0][1], self.issues[0][2]) \
                .pack()
            del self.issues[0]
            self.row += 1
            if self.issues:
                self.config(text=f"{self.title} Issues ({len(self.issues)} more)")
            else:
                self.config(text=f"{self.title} Issues")
        if not self.winfo_children():
            ttk.Label(self, text="No more issues for this team.", foreground="grey").pack()


class IssueRow(ttk.Frame):
    """
    Represents a row displayed in the New Issues and Done Issues frames.
    The row contains the link to the Jira issue, summary, and three buttons (Added, Ignore, and Leave
    for Later).
    After the user clicks on the button for the action they wish to perform, the row is removed from
    the frame, and the next one (if any) is displayed.
    """

    def __init__(self, parent, issue_nbr, summary, status, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.issue_nbr = issue_nbr
        self.status = status
        self.link = ttk.Label(self, text=issue_nbr, foreground="blue",
                              font=('Arial', 10, 'underline'), cursor="hand2")
        self.link.grid(row=0, column=0, padx=5, pady=5)
        self.link.bind('<Button-1>', self.open_link)
        ttk.Label(self, text=summary, wraplength=250).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self, text="Added", command=self.add).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self, text="Ignore", command=self.ignore).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(self, text="Leave for Later", command=self.leave).grid(row=0, column=4, padx=5, pady=5)

    def open_link(self, event):
        """
        Opens the link to the Jira issue in the user's default browser.
        """
        webbrowser.open_new(f"https://jira-doc-tracker.atlassian.net/browse/{self.issue_nbr}")

    def add(self):
        """
        Indicates that the user has manually added the issue to the Ticket sheet because it may
        potentially need to be documented.
        This method adds the issue number to the issues_in_sheet table in the database.
        """
        session = get_session()
        session.add(IssuesInSheet(id=self.issue_nbr))
        session.commit()
        session.close()
        self.destroy()
        self.parent.display_issue()

    def ignore(self):
        """
        Indicates that the user decided to ignore the issue for now because they think it should not
        be documented.
        This method adds the issue number to the ignored_issues table of the database or updates its
        status if the issue is already listed there.
        """
        session = get_session()
        if session.query(IgnoredIssues).filter_by(id=self.issue_nbr).first():
            session.query(IgnoredIssues).filter_by(id=self.issue_nbr).first().status = self.status
        else:
            session.add(IgnoredIssues(id=self.issue_nbr, status=self.status))
        session.commit()
        session.close()
        self.destroy()
        self.parent.display_issue()

    def leave(self):
        """
        Indicates that the user has not made any decision regarding the issue and might therefore wish
        to review it later.
        This method only removes the row from the frame, which means that this issue will be treated
        as new the next time the frame is populated.
        """
        self.destroy()
        self.parent.display_issue()


if __name__ == "__main__":
    # Run the front-end application with the Initial View displayed
    root = tk.Tk()
    InitialView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
