import subprocess
import re
from datetime import datetime, timezone

def get_git_tags():
    # Get the Git tags
    git_tags = subprocess.check_output(['git', 'tag', '--sort=-creatordate'])
    git_tags = git_tags.decode('utf-8').split('\n')
    return git_tags

def get_commit_logs():
    # Get the commit logs using Git
    git_logs = subprocess.check_output(['git', 'log', '--pretty=format:%h,%an,%ae,%ad,%s', '--date=iso'])
    git_logs = git_logs.decode('utf-8').split('\n')
    return git_logs

def extract_dora_metrics(commit_logs, git_tags):
    dora_metrics = {
        'total_commits': 0,
        'authors': set(),
        'last_commit_date': None,
        'average_commits_per_day': 0,
        'time_between_releases': None
    }

    for log in commit_logs:
        match = re.match(r'^([^,]+),([^,]+),([^,]+),([^,]+),(.+)$', log)
        if match:
            commit_date_str = match.group(4)
            try:
                commit_date = datetime.strptime(commit_date_str, "%Y-%m-%d %H:%M:%S %z")
            except ValueError:
                print("Error parsing commit date:", commit_date_str)
                continue

            dora_metrics['total_commits'] += 1
            dora_metrics['authors'].add(match.group(2))
            if not dora_metrics['last_commit_date'] or commit_date > dora_metrics['last_commit_date']:
                dora_metrics['last_commit_date'] = commit_date

    if dora_metrics['total_commits'] > 0:
        days_since_last_commit = (datetime.now(timezone.utc) - dora_metrics['last_commit_date']).days
        dora_metrics['average_commits_per_day'] = dora_metrics['total_commits'] / max(days_since_last_commit, 1)

    if len(git_tags) >= 2:
        tag_dates = []
        for tag in git_tags[:2]:
            try:
                tag_date = subprocess.check_output(['git', 'log', '-1', '--format=%ai', tag])
                tag_date = tag_date.decode('utf-8').strip()
                tag_dates.append(datetime.strptime(tag_date, "%Y-%m-%d %H:%M:%S %z"))
            except ValueError:
                print("Error parsing tag date:", tag_date)
                continue
        
        if len(tag_dates) == 2:
            dora_metrics['time_between_releases'] = tag_dates[0] - tag_dates[1]

    return dora_metrics

if __name__ == '__main__':
    commit_logs = get_commit_logs()
    git_tags = get_git_tags()
    dora_metrics = extract_dora_metrics(commit_logs, git_tags)

    print("DORA Metrics:")
    print("Total Commits:", dora_metrics['total_commits'])
    print("Unique Authors:", len(dora_metrics['authors']))
    print("Last Commit Date:", dora_metrics['last_commit_date'])
    print("Average Commits per Day:", dora_metrics['average_commits_per_day'])
    print("Time Between Releases:", dora_metrics['time_between_releases'])
