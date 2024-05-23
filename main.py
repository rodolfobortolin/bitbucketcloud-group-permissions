import requests
from requests.auth import HTTPBasicAuth
import logging
import os
import csv

# Configuration for authorization and base URL
config = {
    'username': '',
    'token': '',
    'base_url': 'https://api.bitbucket.org',
    'workspace': ''  # Replace with your workspace
}

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Constants for Bitbucket API
REPOS_ENDPOINT = f"{config['base_url']}/2.0/repositories/{config['workspace']}"
PROJECTS_ENDPOINT = f"{config['base_url']}/2.0/workspaces/{config['workspace']}/projects"
REPO_PERMISSIONS_ENDPOINT = f"{config['base_url']}/2.0/repositories/{config['workspace']}/{{repo_slug}}/permissions-config/groups"
PROJECT_PERMISSIONS_ENDPOINT = f"{config['base_url']}/2.0/workspaces/{config['workspace']}/projects/{{project_key}}/permissions-config/groups"
PAGE_LIMIT = 100

# Get the directory of the current script
script_location = os.path.dirname(os.path.abspath(__file__))

def get_repositories(auth):
    repos = []
    url = REPOS_ENDPOINT
    while url:
        response = requests.get(url, auth=auth, headers={"Accept": "application/json"})
        if response.status_code == 200:
            data = response.json()
            repos.extend(data['values'])
            url = data.get('next')
        else:
            logging.error(f"Failed to fetch repositories: {response.status_code} {response.text}")
            break
    logging.info(f"Total repositories fetched: {len(repos)}")
    return repos

def get_projects(auth):
    projects = []
    url = PROJECTS_ENDPOINT
    while url:
        response = requests.get(url, auth=auth, headers={"Accept": "application/json"})
        if response.status_code == 200:
            data = response.json()
            projects.extend(data['values'])
            url = data.get('next')
        else:
            logging.error(f"Failed to fetch projects: {response.status_code} {response.text}")
            break
    logging.info(f"Total projects fetched: {len(projects)}")
    return projects

def get_repo_permissions(auth, repo_slug):
    permissions = []
    url = REPO_PERMISSIONS_ENDPOINT.format(repo_slug=repo_slug)
    while url:
        response = requests.get(url, auth=auth, headers={"Accept": "application/json"})
        if response.status_code == 200:
            data = response.json()
            permissions.extend(data['values'])
            url = data.get('next')
        else:
            logging.error(f"Failed to fetch permissions for repository {repo_slug}: {response.status_code} {response.text}")
            break
    logging.info(f"Total permissions fetched for repository {repo_slug}: {len(permissions)}")
    return permissions

def get_project_permissions(auth, project_key):
    permissions = []
    url = PROJECT_PERMISSIONS_ENDPOINT.format(project_key=project_key)
    while url:
        response = requests.get(url, auth=auth, headers={"Accept": "application/json"})
        if response.status_code == 200:
            data = response.json()
            permissions.extend(data['values'])
            url = data.get('next')
        else:
            logging.error(f"Failed to fetch permissions for project {project_key}: {response.status_code} {response.text}")
            break
    logging.info(f"Total permissions fetched for project {project_key}: {len(permissions)}")
    return permissions

def main():
    auth = HTTPBasicAuth(config['username'], config['token'])
    repositories = get_repositories(auth)
    projects = get_projects(auth)

    csv_file_path = os.path.join(script_location, 'permissions.csv')
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['type', 'slug_or_key', 'group_name', 'read_permission', 'write_permission', 'admin_permission'])

        # Fetch and write repository permissions
        for repo in repositories:
            repo_slug = repo['slug']
            permissions = get_repo_permissions(auth, repo_slug)
            for permission in permissions:
                group_name = permission['group']['name'] if 'group' in permission else 'N/A'
                read_permission = 'read' in permission['permission'] if 'permission' in permission else False
                write_permission = 'write' in permission['permission'] if 'permission' in permission else False
                admin_permission = 'admin' in permission['permission'] if 'permission' in permission else False
                writer.writerow(['repository', repo_slug, group_name, read_permission, write_permission, admin_permission])

        # Fetch and write project permissions
        for project in projects:
            project_key = project['key']
            permissions = get_project_permissions(auth, project_key)
            for permission in permissions:
                group_name = permission['group']['name'] if 'group' in permission else 'N/A'
                read_permission = 'read' in permission['permission'] if 'permission' in permission else False
                write_permission = 'write' in permission['permission'] if 'permission' in permission else False
                admin_permission = 'admin' in permission['permission'] if 'permission' in permission else False
                writer.writerow(['project', project_key, group_name, read_permission, write_permission, admin_permission])

    logging.info(f"Permissions written to CSV file at {csv_file_path}")

if __name__ == "__main__":
    main()
