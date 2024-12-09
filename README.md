# Intermediate
Intermediate repo


## Supabase Tables Overview
### translation_process table:

Fields: id, pr_name, pr_number, source_repo_name, source_pr_name, source_pr_number created_at.
This acts as a summary or aggregator (intermediate) of PR information and stores detailed PRs information from different sources/repos..

## Aggregator Processing:
Extracts the first line (current pr_name, pr_number).
Source Processing:
Parses the second line (split by |) into individual JSON objects, each representing a source record (repo name, source pr name and number).

## Secrets:
Use SUPABASE_SERVICE_KEY for authentication.

