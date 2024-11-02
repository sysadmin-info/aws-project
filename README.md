# AWS Project

## Overview
This project is designed to automate the deployment and management of infrastructure and applications using AWS and Ansible. It includes a set of Ansible playbooks and roles to configure servers and deploy applications efficiently.

## Project Structure
```
aws-project/
│
├── inventory/
│   └── hosts                    # Inventory file listing servers
│
├── playbooks/
│   ├── deploy_app.yml           # Main playbook to deploy the application
│   └── roles/
│       ├── db_server/           # Role to configure the database server
│       │   ├── handlers/
│       │   │   └── main.yml     # Handlers for the db_server role
│       │   ├── tasks/
│       │   │   └── main.yml     # Tasks for the db_server role
│       │   └── vars/
│       │       └── main.yml     # Database variables for db_server role
│       └── web_server/          # Role to configure the web server
│           ├── handlers/
│           │   └── main.yml     # Handlers for the web_server role
│           ├── tasks/
│           │   ├── app.py       # Application script for the web server
│           │   └── main.yml     # Tasks for the web server role
│           └── vars/
│               └── main.yml     # Database variables for web_server role
│
├── vars/
│   └── creds.yml                # Encrypted credentials file using Ansible Vault
│
├── .git/                        # Git version control directory
├── .gitignore                   # Specifies files to ignore in version control
└── README.md                    # Project documentation
```

### .gitignore Content
```
vars/creds.yml
playbooks/roles/*/vars/main.yml
```

## Features
- **Inventory Management**: The `inventory/hosts` file defines the infrastructure resources.
- **Modular Roles**: The `roles/` directory contains reusable Ansible roles for configuring the database and web servers.
- **Deployment Automation**: The `deploy_app.yml` playbook automates the deployment process.
- **Encrypted Variables**: Sensitive credentials in `vars/creds.yml` are encrypted using Ansible Vault for security.

## Prerequisites
- **Ansible**: Ensure you have Ansible installed on your control machine.
- **AWS Credentials**: Set up AWS CLI and configure your AWS credentials.

## Creating `vars/creds.yml`
1. **Purpose**: The `vars/creds.yml` file contains sensitive AWS credentials required for deploying resources. It should include your AWS Access Key, Secret Key, and the AWS region.
2. **Example Structure**:
   ```yaml
   # vars/creds.yml
   aws_access_key: YOUR_AWS_ACCESS_KEY
   aws_secret_key: YOUR_AWS_SECRET_KEY
   aws_region: YOUR_AWS_REGION
   ```
3. **Encrypting `vars/creds.yml`**:
   - Use Ansible Vault to encrypt this file for secure storage and usage.
   - Command to encrypt:
     ```bash
     ansible-vault encrypt vars/creds.yml
     ```
   - You will be prompted to enter a password, which will be required when running Ansible playbooks.

## Database Variables in `vars/main.yml` in Roles
- The `vars/main.yml` files inside the `db_server` and `web_server` roles contain database connection details such as:
  - **Database Name**: Name of the database.
  - **Username & Password**: Credentials for accessing the database.
  - **Host & Port**: Details for connecting to the database server.
- Customize these variables to suit your environment before running the playbooks.

## Usage
1. Update the `inventory/hosts` file with your server details.
2. Run the main playbook to deploy the application, providing the Vault password when prompted:
   ```bash
   ansible-playbook -i inventory/hosts playbooks/deploy_app.yml --ask-vault-pass
   ```

## Directory Details
- **inventory/hosts**: Defines the servers and groups used by Ansible.
- **playbooks/deploy_app.yml**: The primary playbook for deploying the application.
- **roles/db_server**: Contains tasks, handlers, and variables for setting up a database server.
- **roles/web_server**: Contains tasks, handlers, and variables for setting up a web server.
- **vars/creds.yml**: Encrypted credentials managed with Ansible Vault.

## Contributing
Feel free to open issues or submit pull requests if you want to contribute to this project. Follow the contribution guidelines and coding standards.

## License
This project is licensed under MIT LICENSE. See [LICENSE](https://github.com/sysadmin-info/aws-project/blob/main/LICENSE) for more details.

