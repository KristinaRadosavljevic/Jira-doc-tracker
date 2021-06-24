import tkinter as tk
from tkinter import ttk


class InitialView(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Jira Documentation Tracker")
        ttk.Button(self, text="Add a New Project", command=self.add_project)\
            .grid(row=0, column=0, padx=20, pady=20)
        ttk.Button(self, text="Update All Sheets", command=self.update_sheets)\
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


class NewProject(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
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
        ttk.Button(self, text="Back", command=self.back)\
            .grid(row=3, column=3, padx=20, pady=10)

    def back(self):
        self.destroy()
        InitialView(self.parent).pack(side="top", fill="both", expand=True)


class UpdateSheets(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Update All Sheets")


class JiraIssues(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("Review Jira Issues")


if __name__ == "__main__":
    root = tk.Tk()
    InitialView(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
