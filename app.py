import os
import requests
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('GITHUB_USER')
token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}

url = f'https://api.github.com/users/{user}/events'

contributions = defaultdict(list)

page = 1
while True:
    response = requests.get(url, headers=headers, params={'page': page, 'per_page': 100})
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        break

    events = response.json()
    if not events:
        break

    if isinstance(events, dict) and 'message' in events:
        print(f"GitHub API error: {events['message']}")
        break

    if not isinstance(events, list):
        print("Unexpected response format")
        break

    for event in events:
        if 'type' in event and event['type'] in ['PushEvent', 'PullRequestEvent']:
            contributions[event['repo']['name']].append(event['type'])

    page += 1

unique_repos = list(contributions.keys())

print(f'Total open source projects contributed to: {len(unique_repos)}')
print("List of open source projects contributed to with specific contributions:")
for repo in unique_repos:
    print(f"\nRepository: {repo}")
    for contribution in contributions[repo]:
        print(f" - {contribution}")
        
