import requests
import json
import re

WAKATIME_API_KEY = waka_0a76569b-e7d7-4a34-9ff4-931972af9212 # This will be replaced by the environment variable
README_FILE = 'README.md'

def fetch_wakatime_stats(api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    url = 'https://wakatime.com/api/v1/users/current/stats/last_7_days'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Failed to fetch WakaTime stats: {response.status_code}')
        return None

def generate_wakatime_badge(stats):
    total_seconds = stats['data']['grand_total']['total_seconds']
    total_hours = round(total_seconds / 3600, 2)
    return f"![WakaTime](https://wakatime.com/badge/user/{stats['data']['user']['id']}/projects.svg)"

def update_readme(badge_markdown):
    with open(README_FILE, 'r') as file:
        readme_content = file.read()

    # Remove existing WakaTime badge if it exists
    readme_content = re.sub(r'!\[WakaTime\]\(https://wakatime\.com/badge/user/.+?\)', '', readme_content)

    # Insert the new WakaTime badge
    if '### 📊 WakaTime Stats:' in readme_content:
        readme_content = readme_content.replace(
            '### 📊 WakaTime Stats:',
            f'### 📊 WakaTime Stats:\n\n{badge_markdown}'
        )
    else:
        # If the section doesn't exist, add it at the end
        readme_content += f'\n\n### 📊 WakaTime Stats:\n\n{badge_markdown}\n'

    with open(README_FILE, 'w') as file:
        file.write(readme_content)

def main():
    stats = fetch_wakatime_stats(WAKATIME_API_KEY)
    if stats:
        badge_markdown = generate_wakatime_badge(stats)
        update_readme(badge_markdown)
        print('WakaTime stats updated successfully.')
    else:
        print('No stats to update.')

if __name__ == '__main__':
    main()
