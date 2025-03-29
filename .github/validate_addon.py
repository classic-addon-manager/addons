import yaml
import json
import sys
import re
from typing import List, Dict, Any

def validate_addon(addon: Dict[str, Any]) -> List[str]:
    """
    Validates a single addon entry and returns a list of validation errors.
    """
    errors = []
    
    # Required fields check
    required_fields = ['name', 'alias', 'description', 'author', 'repo', 'branch', 'tags']
    optional_fields = ['dependencies', 'kofi']
    
    # Check required fields
    for field in required_fields:
        if field not in addon:
            errors.append(f"Missing required field: {field}")
        elif not addon[field]:  # Check if field is empty
            errors.append(f"Required field '{field}' cannot be empty")
    
    # Name validation (no spaces)
    if 'name' in addon and ' ' in addon['name']:
        errors.append(f"Name field '{addon['name']}' contains spaces")
    
    # Repo format validation (username/reponame)
    if 'repo' in addon and addon['repo']:
        repo_pattern = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')
        if not repo_pattern.match(addon['repo']):
            errors.append(f"Repo field '{addon['repo']}' must be in format 'username/reponame'")
    
    # Tags/categories validation (max 4)
    if 'tags' in addon:
        if not isinstance(addon['tags'], list):
            errors.append("Tags field must be a list")
        elif len(addon['tags']) > 4:
            errors.append(f"Too many categories/tags: {len(addon['tags'])} (maximum is 4)")
        elif not addon['tags']:  # Check if tags list is empty
            errors.append("Tags list cannot be empty")
    
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
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Try parsing YAML
            try:
                addon_data = yaml.safe_load(content)
            except yaml.YAMLError as e:
                all_errors.append(f"Invalid YAML in {file_path}: {str(e)}")
                continue
            
            # Validate the addon entry
            if isinstance(addon_data, dict):
                errors = validate_addon(addon_data)
                if errors:
                    all_errors.extend([f"{file_path}: {error}" for error in errors])
                    
        except Exception as e:
            all_errors.append(f"Error processing {file_path}: {str(e)}")
    
    return all_errors

def main():
    # Get list of changed files from command line arguments
    changed_files = sys.argv[1:]
    
    # Validate the changes
    errors = validate_pr_changes(changed_files)
    
    # Output results in GitHub Actions format
    if errors:
        print("::error::Validation errors found:")
        for error in errors:
            print(f"::error::{error}")
        sys.exit(1)
    else:
        print("::notice::All validations passed!")
        sys.exit(0)

if __name__ == "__main__":
    main() 