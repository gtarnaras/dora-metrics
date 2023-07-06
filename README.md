# gut-dora

# What is

If DevOps is a philosophy then we have to assume that if you are working as a DevOps philosopher, you usually know how fast or slow you release to production! But how can we measure that? With gut-dora! Turn that gut feeling into git-based metrics! This script extracts very simple DORA metrics and KPIs from git-based repos, providing insights into commit history and release metrics. 

`git + gut feeling for DORA = gut-dora (see what I did there...?)`

**But Sensei, what are DORA metrics?**

If you haven't heard of DORA, then I suggest yuo read this article -> https://cloud.google.com/blog/products/devops-sre/using-the-four-keys-to-measure-your-devops-performance . Then this repo might make sense, or may not!


## Description

The gut-dora script retrieves commit logs from a Git repository and calculates various metrics, including:

- Total number of commits
- Unique authors
- First and last commit dates
- Average commits per day
- Time between releases (based on Git tags)

## Usage

1. Ensure you have Python installed on your system.
2. Clone the repository or copy the script code into a local file.
3. Open a terminal or command prompt and navigate to the directory containing the script.
4. Run the script using the following command:

```
python gut-dora.py
```

## Contributions

Raise a PR!
