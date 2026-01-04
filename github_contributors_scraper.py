import requests
from bs4 import BeautifulSoup

def scrape_contributors(repo_owner, repo_name, include=None, exclude=None):
    """
    Scrapes the contributors list from a GitHub repository page.

    :param repo_owner: Owner of the repository
    :param repo_name: Name of the repository
    :param include: List of usernames to force include (optional)
    :param exclude: List of usernames to exclude (optional)
    :return: List of contributor usernames
    """
    url = f"https://github.com/{repo_owner}/{repo_name}/graphs/contributors"
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all contributor usernames based on the <a> tag structure
    contributors = []
    for user in soup.select('a[href^="/"][class^="prc-Link-Link"]'):
        username = user.text.strip()
        if username and username not in contributors:
            contributors.append(username)

    # Include additional usernames
    if include:
        contributors.extend(user for user in include if user not in contributors)

    # Exclude specified usernames
    if exclude:
        contributors = [user for user in contributors if user not in exclude]

    return contributors

# Example usage
repo_owner = "torvalds"  # Change this to your repo owner
repo_name = "linux"  # Change this to your repo name
include_list = ["extraUser1", "extraUser2"]
exclude_list = ["someUserToExclude"]

contributors = scrape_contributors(repo_owner, repo_name, include_list, exclude_list)
print(contributors)
