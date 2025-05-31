import yaml
import json
import sys
import re
import requests

from typing import List, Dict, Any

def validate_addon(addon: Dict[str, Any]) -> List[str]:
    """
    Validates a single addon entry and returns a list of validation errors.
    """
    errors = []
    
    # Required fields check
    required_fields = ['name', 'alias', 'description', 'author', 'repo', 'branch', 'tags']
    optional_fields = ['dependencies', 'kofi', 'keywords']
    
    # Check required fields
    for field in required_fields:
        if field not in addon:
            errors.append(f"Missing required field: {field}")
        elif addon[field] is None or addon[field] == '':  # Check if field is empty
            errors.append(f"Required field '{field}' cannot be empty")
        elif isinstance(addon[field], bool):  # Check if field is boolean instead of string
            errors.append(f"Field '{field}' must be a string, not a boolean")
    
    # Name validation (no spaces)
    if 'name' in addon and addon['name'] is not None:
        if isinstance(addon['name'], bool):
            # Already captured above, skip to avoid duplicate errors
            pass
        elif not isinstance(addon['name'], str):
            errors.append(f"Name field must be a string, got {type(addon['name']).__name__}")
        elif ' ' in addon['name']:
            errors.append(f"Name field '{addon['name']}' contains spaces")
    
    # Repo format validation (username/reponame)
    repo_valid_format = False
    if 'repo' in addon and addon['repo'] is not None:
        if isinstance(addon['repo'], bool):
            # Already captured above, skip to avoid duplicate errors
            pass
        elif not isinstance(addon['repo'], str):
            errors.append(f"Repo field must be a string, got {type(addon['repo']).__name__}")
        elif addon['repo']: # Only validate non-empty strings
            repo_pattern = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')
            if not repo_pattern.match(addon['repo']):
                errors.append(f"Repo field '{addon['repo']}' must be in format 'username/reponame'")
            else:
                repo_valid_format = True # Mark format as valid for release check

    # GitHub Release check (only if repo format is valid)
    if repo_valid_format:
        repo_name = addon['repo']
        api_url = f"https://api.github.com/repos/{repo_name}/releases"
        try:
            response = requests.get(api_url, headers={'Accept': 'application/vnd.github.v3+json'}, timeout=10)
            if response.status_code == 200:
                releases = response.json()
                if not releases:
                    errors.append(f"Repository '{repo_name}' must have at least one release on GitHub.")
            elif response.status_code == 404:
                errors.append(f"Repository '{repo_name}' not found on GitHub.")
            elif response.status_code == 403: # Rate limit or other access issue
                 print(f"::warning::Could not check releases for {repo_name} due to GitHub API rate limit or access issue. Status: {response.status_code}. Response: {response.text}")
                 # Optionally add a warning instead of an error, or skip the check
                 # errors.append(f"Could not verify releases for '{repo_name}' due to GitHub API limitations.")
            else:
                errors.append(f"Failed to fetch releases for '{repo_name}'. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            errors.append(f"Error checking GitHub releases for '{repo_name}': {e}")    # Tags/categories validation (max 4)
    if 'tags' in addon:
        if not isinstance(addon['tags'], list):
            if isinstance(addon['tags'], bool):
                errors.append("Tags field must be a list, not a boolean")
            else:
                errors.append(f"Tags field must be a list, got {type(addon['tags']).__name__}")
        elif len(addon['tags']) > 4:
            errors.append(f"Too many categories/tags: {len(addon['tags'])} (maximum is 4)")
        elif not addon['tags']:  # Check if tags list is empty
            errors.append("Tags list cannot be empty")
        else:
            # Validate each tag is a string
            for i, tag in enumerate(addon['tags']):
                if not isinstance(tag, str):
                    errors.append(f"Tag at position {i+1} must be a string, got {type(tag).__name__}")
    
    # Keywords validation
    if 'keywords' in addon:
        if not isinstance(addon['keywords'], list):
            if isinstance(addon['keywords'], bool):
                errors.append("Keywords field must be a list, not a boolean")
            else:
                errors.append(f"Keywords field must be a list, got {type(addon['keywords']).__name__}")
        else:
            # Validate each keyword is a string and contains no spaces
            for i, keyword in enumerate(addon['keywords']):
                if not isinstance(keyword, str):
                    errors.append(f"Keyword at position {i+1} must be a string, got {type(keyword).__name__}")
                elif ' ' in keyword:
                    errors.append(f"Keyword at position {i+1} '{keyword}' cannot contain spaces")
            
            # Check concatenated string length (only if all keywords are valid strings)
            if all(isinstance(keyword, str) for keyword in addon['keywords']):
                concatenated_keywords = ' '.join(addon['keywords'])
                if len(concatenated_keywords) > 255:
                    errors.append(f"Keywords concatenated string length ({len(concatenated_keywords)} characters) exceeds 255 character limit")
    
    # Validate that no unknown fields are present
    all_valid_fields = required_fields + optional_fields
    unknown_fields = [field for field in addon.keys() if field not in all_valid_fields]
    if unknown_fields:
        errors.append(f"Unknown fields found: {', '.join(unknown_fields)}")
    
    return errors

def validate_pr_changes(pr_files: List[str]) -> List[str]:
    """
    Validates all changed YAML files in the PR.
    """
    all_errors = []
    
    for file_path in pr_files:
        if not file_path.endswith('.yml') and not file_path.endswith('.yaml'):
            continue
            
        try:
            # Get filename without extension and directory path
            filename = file_path.split('/')[-1]
            filename_without_ext = filename.rsplit('.', 1)[0]

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Try parsing YAML
            try:
                print(f"Processing file: {file_path}")
                # Force string interpretation for scalar values
                def string_constructor(loader, node):
                    if isinstance(node, yaml.ScalarNode):
                        value = loader.construct_scalar(node)
                        return str(value)
                    return loader.construct_scalar(node)
                def sequence_constructor(loader, node):
                    result = loader.construct_sequence(node)
                    return [str(item) if not isinstance(item, (list, dict)) else item for item in result]
                # Add our custom constructors
                yaml.add_constructor('tag:yaml.org,2002:str', string_constructor)
                yaml.add_constructor('tag:yaml.org,2002:seq', sequence_constructor)
                # Print raw content for debugging
                print(f"Raw content:\n{content}")
                addon_data = yaml.safe_load(content)
                print(f"Parsed data: {addon_data}")
                if addon_data is None:
                    all_errors.append(f"Empty YAML file: {file_path}")
                    continue
                if not isinstance(addon_data, dict):
                    all_errors.append(f"Invalid YAML structure in {file_path}: expected a dictionary/object, got {type(addon_data).__name__}")
                    continue

                # Check if filename matches the name field
                if 'name' in addon_data and addon_data['name'] is not None:
                    if filename_without_ext != addon_data['name']:
                        all_errors.append(f"[{file_path}] Filename '{filename_without_ext}' must match the 'name' field '{addon_data['name']}'")

            except yaml.YAMLError as e:
                print(f"Raw YAML error: {str(e)}")
                all_errors.append(f"Invalid YAML syntax in {file_path}: {str(e)}")
                continue
            
            # Validate the addon entry
            try:
                errors = validate_addon(addon_data)
                if errors:
                    # Prefix errors with file name for clarity
                    prefixed_errors = [f"[{file_path}] {error}" for error in errors]
                    all_errors.extend(prefixed_errors)
            except Exception as e:
                all_errors.append(f"Error validating {file_path}: {str(e)}")
                    
        except Exception as e:
            all_errors.append(f"Error reading or processing file {file_path}: {str(e)}")
    
    return all_errors

def main():
    # Get list of changed files from command line arguments
    changed_files = sys.argv[1:]
    
    # Validate the changes
    errors = validate_pr_changes(changed_files)
    
    # Output results in GitHub Actions format
    if errors:
        print("::error::The following issues were found in your addon submission:")
        for error in errors:
            print(f"::error::{error}")
        sys.exit(1)
    else:
        print("::notice::All validations passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()