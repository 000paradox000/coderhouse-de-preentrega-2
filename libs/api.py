from urllib.parse import urlencode

import pandas as pd
import requests


class APIHandler:
    def get_repos(self, topic: str = "llm") -> pd.DataFrame:
        """Get github repos that contain a topic value."""

        uri = "api.github.com/search/repositories"
        page = 1
        per_page = 20
        qs = urlencode({
            "q": f"{topic}+in:name",
            "page": page,
            "per_page": per_page,
        })

        url = f"https://{uri}?{qs}"
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(url, headers=headers)
        status_code = response.status_code

        if status_code != 200:
            raise ValueError(f"Error fetching data: {status_code}")

        keys = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "html_url",
        ]
        repos = response.json()["items"]
        repos = [{key: d[key] for key in keys} for d in repos]

        return pd.DataFrame(repos)
