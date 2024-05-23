# Bitbucket Permissions Fetcher

This script fetches the permissions for repositories and projects in a Bitbucket workspace and saves them to a CSV file.

## Prerequisites

- Python 3.x
- `requests` library
- `logging` library

## Configuration

You need to set up the configuration with your Bitbucket credentials and workspace details.

1. Open the script file.
2. Update the `config` dictionary with your Bitbucket username, token, and workspace.

```python
config = {
    'username': '<username>',  # Replace with your Bitbucket username
    'token': '<token>',        # Replace with your Bitbucket app password
    'base_url': 'https://api.bitbucket.org',
    'workspace': '<workspace>' # Replace with your workspace name
}
```

## Usage

1. Clone this repository or download the script file.
2. Navigate to the directory containing the script.
3. Run the script using Python:

```bash
python script.py
```

The script will fetch the permissions and save them to a CSV file named permissions.csv in the same directory.

## Output
The CSV file will contain the following columns:

- `type`: Indicates whether the entry is for a repository or a project.
- `slug_or_key`: The slug of the repository or the key of the project.
- `group_name`: The name of the group.
- `read_permission`: Whether the group has read permission.
- `write_permission`: Whether the group has write permission.
- `admin_permission`: Whether the group has admin permission.
- Empty strings will be used to indicate the absence of permissions.

## Example
```csv
|type         |slug_or_key     |group_name|read_permission           |write_permission|admin_permission|
|-------------|----------------|----------|--------------------------|----------------|----------------|
|repository   |repo1           |group1    |read                      |                |admin           |
|repository   |repo2           |group2    |                          |                |admin           |
|project      |proj1           |group1    |read                      |write           |                |
|project      |proj2           |group2    |read                      |                |                |
```
