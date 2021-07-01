import tkinter as tk
from tkinter import ttk
import webbrowser


class InitialView(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Jira Documentation Tracker")
        ttk.Button(self, text="Add a New Project", command=self.add_project)\
            .grid(row=0, column=0, padx=20, pady=20)
        ttk.Button(self, text="Update the Sheet", command=self.update_sheets)\
            .grid(row=0, column=1, pady=20)
        ttk.Button(self, text="Review Jira Issues", command=self.review_issues)\
            .grid(row=0, column=2, padx=20, pady=20)

    def add_project(self):
        self.destroy()
        NewProject(self.parent).pack(side="top", fill="both", expand=True)

    def update_sheets(self):
        self.destroy()
        UpdateSheets(self.parent).pack(side="top", fill="both", expand=True)

    def review_issues(self):
        self.destroy()
        JiraIssues(self.parent).pack(side="top", fill="both", expand=True)


class SecondaryView(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.back_button = ttk.Button(self, text="Back", command=self.back)

    def back(self):
        self.destroy()
        InitialView(self.parent).pack(side="top", fill="both", expand=True)

    def team_frame(self, label, command):
        input_frame = ttk.Frame(self, relief="groove", width=350, height=100)
        input_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=10, ipady=10)
        ttk.Label(input_frame, text="Select a team:", justify="center") \
            .grid(row=0, column=0, padx=15, pady=5)
        team = tk.StringVar()
        teams = ("Team A", "Team B", "Team C")
        ttk.Combobox(input_frame, values=teams, state="readonly", textvariable=team) \
            .grid(row=1, column=0, padx=15, pady=5)
        team.set("Team A")
        ttk.Button(input_frame, text=label, command=lambda: command(team.get())) \
            .grid(row=2, column=0, padx=15, pady=5)


class NewProject(SecondaryView):

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Add a New Project")
        ttk.Label(self, text="Enter the release number:")\
            .grid(row=0, column=0, columnspan=5, padx=20, pady=10)
        self.entry = ttk.Entry(self, width=20)
        self.entry.grid(row=1, column=0, columnspan=5, padx=20, pady=10)
        ttk.Label(self,
                  text="Note: Make sure that all the filters for this project are set up in Jira"
                       " and that they are correctly named.",
                  wraplength=350, justify="center", foreground="grey")\
            .grid(row=2, column=0, columnspan=5, padx=20, pady=10)
        ttk.Button(self, text="Enter")\
            .grid(row=3, column=1, padx=20, pady=10)
        self.back_button.grid(row=3, column=3, padx=20, pady=10)


class UpdateSheets(SecondaryView):

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Update the Sheet")
        self.team_frame("Update", self.update_sheet)
        ttk.Label(self, text="- or -", justify="center")\
            .grid(row=1, column=0, columnspan=2)
        ttk.Button(self, text="Update All Sheets")\
            .grid(row=2, column=0, columnspan=2, padx=20, pady=15)
        self.back_button.grid(row=3, column=1, padx=20, pady=10, sticky="e")

    def update_sheet(self, team):
        pass


class JiraIssues(SecondaryView):

    def __init__(self, parent, *args, **kwargs):
        SecondaryView.__init__(self, parent, *args, **kwargs)
        self.parent.title("Review Jira Issues")
        self.team_frame("Find Issues", self.find_issues)
        self.new_frame = ttk.LabelFrame(self, text="New Issues")
        self.new_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10, ipady=10)
        self.new_ph = ttk.Label(self.new_frame, text="Select a team and click 'Find Issues'.",
                                foreground="grey")
        self.new_ph.grid(row=0, column=0, padx=10, pady=10)
        self.done_frame = ttk.LabelFrame(self, text="Done Issues")
        self.done_frame.grid(row=2, column=0, columnspan=2, padx=15, pady=10, ipady=10)
        ttk.Label(self.done_frame, text="Select a team and click 'Find Issues'.", foreground="grey") \
            .grid(row=0, column=0, padx=10, pady=10)

    def find_issues(self, team):
        self.new_ph.destroy()
        label = IssueRow(self.new_frame, "PC-2", "Summary", "Kristina", "Done")
        label.grid(row=0, column=0)


class IssueRow(ttk.Frame):

    def __init__(self, parent, issue_nbr, summary, assignee, status, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.issue_nbr = issue_nbr
        self.link = ttk.Label(self, text=issue_nbr, foreground="blue",
                              font=('Arial', 10, 'underline'), cursor="hand2")
        self.link.grid(row=0, column=0)
        self.link.bind('<Button-1>', self.open_link)

    def open_link(self, event):
        webbrowser.open_new(f"https://jira-doc-tracker.atlassian.net/browse/{self.issue_nbr}")


if __name__ == "__main__":
    root = tk.Tk()
    InitialView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
