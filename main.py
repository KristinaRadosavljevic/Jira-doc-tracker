import requests
from requests.auth import HTTPBasicAuth

from config import username, password

if __name__ == "__main__":
    url = "https://jira-doc-tracker.atlassian.net/rest/api/3/issue/PC-1"

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

    data = response.json()
    summary = data['fields']['summary']

    print(summary)
