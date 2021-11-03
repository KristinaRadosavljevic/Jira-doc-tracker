from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ReleaseNumber(Base):
    __tablename__ = "release_number"

    rn = Column(String, primary_key=True)


class IssuesInSheet(Base):
    __tablename__ = "issues_in_sheet"

    id = Column(String, primary_key=True)


class IgnoredIssues(Base):
    __tablename__ = "ignored_issues"

    id = Column(String, primary_key=True)
    status = Column(String)
