# AWS Cloud-CostReporter

This project is designed to analyze AWS Cost and Usage data, generate visualizations, and provide a detailed cost comparison report in a Microsoft Word document. The tool leverages the AWS Cost Explorer API to retrieve cost data, groups by services, and generates tables and graphs for cost comparisons over the past few months.

## Prerequisites

Before running the project, ensure you have the following:

- Python 3.7 or later installed.
- AWS credentials configured with sufficient permissions to access Cost Explorer data.
- Required Python packages installed (see [Installation](#installation)).

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/bestcloudforme/Cloud-CostReporter.git
    cd Cloud-CostReporter
    ```

2. Install the required dependencies using pip:

    ```bash
    pip3 install -r requirements.txt
    ```

    **Required Python libraries:**
    - `boto3`: AWS SDK for Python to interact with Cost Explorer.
    - `matplotlib`: Used for generating cost comparison graphs.
    - `python-docx`: For generating the Word report.

3. Configure your AWS credentials with the appropriate permissions (e.g., via `~/.aws/credentials` or environment variables).

## Usage

Run the main script to fetch AWS cost data, process it, and generate the report.

```bash
python cost-reporter.py
```
## Helpful Links

- [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html): Step-by-step instructions for installing AWS CLI.
- [awsx](https://github.com/mertongngl/awsx): For orchestration in CLI configurations of multiple AWS accounts.

