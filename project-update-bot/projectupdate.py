#!/usr/bin/env python3
"""
GitHub Repository Auto-Updater for Portfolio
Fetches user repositories and generates a JSON file for portfolio display
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

class GitHubRepoFetcher:
    def __init__(self, github_username: str, github_token: str = None):
        """
        Initialize the GitHub repo fetcher
        
        Args:
            github_username: GitHub username
            github_token: GitHub personal access token (optional, for higher rate limits)
        """
        self.username = github_username
        self.token = github_token
        self.api_base = "https://api.github.com"
        self.headers = self._get_headers()
    
    def _get_headers(self) -> dict:
        """Prepare headers for API requests"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Portfolio-Bot"
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers
    
    def fetch_repositories(self, exclude_forks: bool = True) -> list:
        """
        Fetch all repositories for the user
        
        Args:
            exclude_forks: If True, exclude forked repositories
            
        Returns:
            List of repository dictionaries
        """
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.api_base}/users/{self.username}/repos"
            params = {
                "page": page,
                "per_page": per_page,
                "sort": "updated",
                "direction": "desc",
                "type": "all"
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching repositories: {e}")
                break
            
            data = response.json()
            if not data:
                break
            
            for repo in data:
                # Skip forks if requested
                if exclude_forks and repo["fork"]:
                    continue
                
                repos.append(self._process_repo(repo))
            
            # Check if there are more pages
            if "Link" not in response.headers:
                break
            
            page += 1
        
        return repos
    
    def _process_repo(self, repo: dict) -> dict:
        """Process and format repository data"""
        return {
            "id": repo["id"],
            "name": repo["name"],
            "description": repo["description"] or "No description provided",
            "url": repo["html_url"],
            "homepage": repo["homepage"],
            "language": repo["language"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "updated_at": repo["updated_at"],
            "created_at": repo["created_at"],
            "topics": repo["topics"],
            "is_private": repo["private"],
        }
    
    def generate_json(self, repos: list, output_path: str = "../repositories.json") -> bool:
        """
        Generate JSON file with repository data
        
        Args:
            repos: List of repository dictionaries
            output_path: Path where to save the JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_file = Path(__file__).parent.parent / "repositories.json"
            
            data = {
                "generated_at": datetime.now().isoformat(),
                "total_repos": len(repos),
                "repositories": repos
            }
            
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Successfully generated {output_file}")
            print(f"  Total repositories: {len(repos)}")
            return True
            
        except Exception as e:
            print(f"✗ Error generating JSON: {e}")
            return False


def main():
    """Main execution function"""
    # Get credentials from environment variables
    github_username = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_username:
        print("Error: GITHUB_USERNAME environment variable not set")
        return False
    
    print(f"Fetching repositories for: {github_username}")
    
    # Initialize fetcher
    fetcher = GitHubRepoFetcher(github_username, github_token)
    
    # Fetch repositories
    repos = fetcher.fetch_repositories(exclude_forks=True)
    
    if not repos:
        print("No repositories found or error occurred")
        return False
    
    print(f"Found {len(repos)} repositories")
    
    # Generate JSON
    success = fetcher.generate_json(repos)
    
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
