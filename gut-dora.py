#!/usr/bin/env python3
"""

    Name:           gut-dora.py
    Author:         George Tarnaras
    Description:    Simple git-based dora metrics and KPIs. 

"""

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
    commit_infos = [re.match(r'^([^,]+),([^,]+),([^,]+),([^,]+),(.+)$', log).groups() for log in commit_logs]
    commit_dates = [datetime.strptime(info[3], "%Y-%m-%d %H:%M:%S %z") for info in commit_infos if info]
    
    total_commits = len(commit_infos)
    authors = {info[1] for info in commit_infos}
    first_commit_date = min(commit_dates) if commit_dates else None
    last_commit_date = max(commit_dates) if commit_dates else None

    average_commits_per_day = total_commits / max((last_commit_date - first_commit_date).days, 1)
    time_between_releases = None

    if len(git_tags) >= 2:
        tag_dates = [subprocess.check_output(['git', 'log', '-1', '--format=%ai', tag]).decode('utf-8').strip() for tag in git_tags[:2]]
        tag_dates = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S %z") for date in tag_dates if date]
        time_between_releases = tag_dates[0] - tag_dates[1] if len(tag_dates) == 2 else None

    return {
        'total_commits': total_commits,
        'authors': authors,
        'first_commit_date': first_commit_date,
        'last_commit_date': last_commit_date,
        'average_commits_per_day': average_commits_per_day,
        'time_between_releases': time_between_releases,
    }

def calculate_kpi_metrics(dora_metrics):
    kpi_metrics = {
        'commit_velocity': 0,
        'commit_stability': 0,
        'release_frequency': 0,
        'time_to_release': None
    }

    if dora_metrics['total_commits'] > 0:
        days_between_commits = (dora_metrics['last_commit_date'] - dora_metrics['first_commit_date']).days
        kpi_metrics['commit_velocity'] = dora_metrics['total_commits'] / max(days_between_commits, 1)

        kpi_metrics['commit_stability'] = len(dora_metrics['authors']) / dora_metrics['total_commits']

        if dora_metrics['average_commits_per_day'] > 0:
            kpi_metrics['release_frequency'] = 1 / dora_metrics['average_commits_per_day']

    kpi_metrics['time_to_release'] = dora_metrics['time_between_releases']

    return kpi_metrics

if __name__ == '__main__':
    commit_logs = get_commit_logs()
    git_tags = get_git_tags()
    dora_metrics = extract_dora_metrics(commit_logs, git_tags)
    kpi_metrics = calculate_kpi_metrics(dora_metrics)

    print("DORA Metrics:")
    print(f"Total Commits: {dora_metrics['total_commits']}")
    print(f"Unique Authors: {len(dora_metrics['authors'])}")
    print(f"First Commit Date: {dora_metrics['first_commit_date']}")
    print(f"Last Commit Date: {dora_metrics['last_commit_date']}")

    print("\nKPI Metrics:")
    print(f"Commit Velocity (Commits/Day): {kpi_metrics['commit_velocity']}")
    print(f"Commit Stability: {kpi_metrics['commit_stability']}")
    print(f"Release Frequency (Days/Release): {kpi_metrics['release_frequency']}")
    print(f"Time to Release: {kpi_metrics['time_to_release']}")



