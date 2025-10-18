#!/usr/bin/env python3
"""
Prompt Injection Mitigation Demo

This script demonstrates prompt injection vulnerabilities and mitigations
using AWS Bedrock Converse API.
"""

import argparse
import json
import sys
from pathlib import Path
import boto3
from botocore.exceptions import ClientError


def find_example_directory(example_arg):
    """
    Find the example directory based on user input.
    Accepts either a number (e.g., "1") or full directory name (e.g., "example_1_normal_usage").
    """
    base_path = Path(__file__).parent

    # If it's just a number, look for example_N_* pattern
    if example_arg.isdigit():
        pattern = f"example_{example_arg}_*"
        matches = list(base_path.glob(pattern))

        if not matches:
            print(f"Error: No example directory found matching 'example_{example_arg}_*'")
            list_available_examples()
            sys.exit(1)

        if len(matches) > 1:
            print(f"Error: Multiple directories match 'example_{example_arg}_*':")
            for match in matches:
                print(f"  - {match.name}")
            sys.exit(1)

        return matches[0]

    # Otherwise, treat it as a directory name
    example_dir = base_path / example_arg
    if not example_dir.exists():
        print(f"Error: Directory '{example_arg}' not found")
        list_available_examples()
        sys.exit(1)

    return example_dir


def list_available_examples():
    """List all available example directories."""
    base_path = Path(__file__).parent
    examples = sorted(base_path.glob("example_*"))

    if examples:
        print("\nAvailable examples:")
        for example in examples:
            # Extract number from directory name
            parts = example.name.split('_')
            if len(parts) >= 2 and parts[1].isdigit():
                number = parts[1]
                print(f"  {number}: {example.name}")
    else:
        print("\nNo example directories found.")


def load_example_files(example_dir):
    """
    Load the required files from an example directory.
    Returns: (system_instructions, user_input, configuration)
    """
    required_files = {
        'system_instructions.txt': 'system instructions',
        'user_input.txt': 'user input',
        'configuration.json': 'configuration'
    }

    # Check all required files exist
    missing_files = []
    for filename in required_files.keys():
        if not (example_dir / filename).exists():
            missing_files.append(filename)

    if missing_files:
        print(f"Error: Missing required files in {example_dir.name}:")
        for filename in missing_files:
            print(f"  - {filename}")
        sys.exit(1)

    # Load system instructions
    with open(example_dir / 'system_instructions.txt', 'r') as f:
        system_instructions = f.read()

    # Load user input
    with open(example_dir / 'user_input.txt', 'r') as f:
        user_input = f.read()

    # Load configuration
    with open(example_dir / 'configuration.json', 'r') as f:
        configuration = json.load(f)

    return system_instructions, user_input, configuration


def call_bedrock_converse(system_instructions, user_input, configuration):
    """
    Call AWS Bedrock Converse API with the provided instructions and input.
    """
    try:
        # Initialize Bedrock client
        bedrock = boto3.client('bedrock-runtime')

        # Build the request
        request_params = {
            'modelId': configuration['modelId'],
            'messages': [
                {
                    'role': 'user',
                    'content': [{'text': user_input}]
                }
            ],
            'system': [{'text': system_instructions}],
            'inferenceConfig': configuration.get('inferenceConfig', {})
        }

        # Call the API
        response = bedrock.converse(**request_params)

        return response

    except ClientError as e:
        print(f"Error calling Bedrock API: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def display_results(example_name, system_instructions, user_input, configuration, response):
    """Display the results in a formatted way."""
    # Extract the text response
    if 'output' in response and 'message' in response['output']:
        message = response['output']['message']
        if 'content' in message:
            for content_block in message['content']:
                if 'text' in content_block:
                    print(content_block['text'])


def main():
    parser = argparse.ArgumentParser(
        description='Prompt Injection Mitigation Demo using AWS Bedrock',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py --example 1                    # Run example 1
  python run.py --example example_1_normal_usage  # Run by directory name
        """
    )

    parser.add_argument(
        '--example',
        type=str,
        help='Example number (e.g., "1") or full directory name (e.g., "example_1_normal_usage")'
    )

    args = parser.parse_args()

    # If no example specified, show help and available examples
    if not args.example:
        parser.print_help()
        list_available_examples()
        sys.exit(0)

    # Find and load the example
    example_dir = find_example_directory(args.example)
    system_instructions, user_input, configuration = load_example_files(example_dir)

    # Call Bedrock API
    response = call_bedrock_converse(system_instructions, user_input, configuration)

    # Display results
    display_results(example_dir.name, system_instructions, user_input, configuration, response)


if __name__ == '__main__':
    main()
