# Prompt Injection Mitigation Demo

Created by [Wayne Workman](https://github.com/wayneworkman)

[![Blog](https://img.shields.io/badge/Blog-wayne.theworkmans.us-blue)](https://wayne.theworkmans.us/)
[![GitHub](https://img.shields.io/badge/GitHub-wayneworkman-181717?logo=github)](https://github.com/wayneworkman)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Wayne_Workman-0077B5?logo=linkedin)](https://www.linkedin.com/in/wayne-workman-a8b37b353/)
[![SpinnyLights](https://img.shields.io/badge/SpinnyLights-wayneworkman-764ba2)](https://spinnylights.com/wayneworkman)

This Terraform module deploys an AWS Lambda function that uses Amazon Bedrock to detect prompt injection attempts in user input. The module implements the security principles outlined in [this hands-on demo](https://wayne.theworkmans.us/posts/2025/10/2025-10-18-prompt-injection-hands-on-demo.html).


A practical demonstration of prompt injection vulnerabilities and mitigation techniques using AWS Bedrock's Converse API.

## What This Project Demonstrates

This project provides three concrete examples that illustrate:

1. **Normal Usage** - How a properly functioning AI assistant should behave
2. **Prompt Injection Attack** - How malicious user input can subvert system instructions
3. **Detection-Based Mitigation** - How to identify and block prompt injection attempts

## Project Structure

Each example is contained in its own directory with three files:

- `system_instructions.txt` - The system prompt that defines the AI's behavior
- `user_input.txt` - The user's input to the system
- `configuration.json` - AWS Bedrock model configuration

### Examples

- **example_1_normal_usage** - Demonstrates legitimate user interaction with an AI assistant that has access to tools
- **example_2_basic_prompt_injection** - Shows how an attacker can override system instructions to extract sensitive information
- **example_3_injection_detection** - Implements a security analyzer that detects prompt injection attempts before processing

## Running the Examples

```bash
# Run by example number
python run.py --example 1
python run.py --example 2
python run.py --example 3

# Or by full directory name
python run.py --example example_1_normal_usage

# List available examples
python run.py
```

## Requirements

- Python 3.x
- boto3
- AWS credentials configured with access to Bedrock
- Access to Claude Sonnet 4.5 model in AWS Bedrock

## Key Takeaways

1. **Prompt injection is real** - System instructions alone are insufficient to prevent determined attackers
2. **Defense requires multiple layers** - Delimiters, validation, and detection work together
3. **Detection models are effective** - Using an LLM to validate input before processing adds significant security
4. **Trade-offs exist** - More security means more API calls, higher latency, and increased cost

For a detailed walkthrough and explanation, see my blog post: [Prompt Injection: A Hands-On Demo](https://wayne.theworkmans.us/posts/2025/10/2025-10-18-prompt-injection-hands-on-demo.html)
