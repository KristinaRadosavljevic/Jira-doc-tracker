# This file contains the functions for connecting to the database and Jira API.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from requests.auth import HTTPBasicAuth

from config import username, password


# Setup for the get_session function
engine = create_engine("sqlite:///doc_tracker.db")
Session = sessionmaker(bind=engine)


def get_session():
    """
    Opens a connection to the sqlalchemy session.
    Use this function when accessing the database.
    """
    return Session()


def api_request(url):
    """
    Basic authentication for Jira API used when retrieving data from Jira.

    Arguments:
        url (str) - The request URL.

    Returns the response from Jira API converted into the JSON format.
    """
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
