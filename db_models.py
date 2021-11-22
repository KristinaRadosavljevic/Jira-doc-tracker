# This file contains the database model.

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ReleaseNumber(Base):
    """
    Contains only one row which stores the current release number.

    Columns:
        rn (str) - The current release number.
    """
    __tablename__ = "release_number"

    rn = Column(String, primary_key=True)


class IssuesInSheet(Base):
    """
    Contains Jira issues which have been manually added to the Ticket workbook.

    Columns:
        id (str) - The issue number.
    """
    __tablename__ = "issues_in_sheet"

    id = Column(String, primary_key=True)


class IgnoredIssues(Base):
    """
    Contains Jira issues which the user has chosen to ignore.

    Columns:
        id (str) - The issue number.
        status (str) - The last known status of the issue.
    """
    __tablename__ = "ignored_issues"

    id = Column(String, primary_key=True)
    status = Column(String)
