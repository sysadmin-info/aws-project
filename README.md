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

## Configuring AWS Security Group
To ensure proper access to your servers and applications, update your AWS Security Group settings:

1. **Allow SSH (Port 22)**: 
   - Source: `0.0.0.0/0` (for internet access)
   - Purpose: Enable remote SSH access to your instances from anywhere. Make sure to restrict this in a production environment for better security.

2. **Allow HTTP (Port 80)**:
   - Source: `0.0.0.0/0` (for internet access)
   - Purpose: Allow public HTTP traffic to the web server.

3. **Allow MySQL (Port 3306)**:
   - Source: `172.16.0.0/12` (for internal network access only)
   - Purpose: Restrict database access to the internal network for security. The `172.16.0.0/12` range covers private IP addresses used for internal communication.

Configure these rules in your AWS Management Console under the "Security Groups" settings for your EC2 instances.

## Creating `vars/creds.yml`
1. **Purpose**: The `vars/creds.yml` file contains sensitive AWS credentials required for deploying resources. It should include your AWS Access Key, Secret Key, and the AWS region.
2. **Example Structure**:
   ```yaml
   # vars/creds.yml
   aws_access_key: "YOUR_AWS_ACCESS_KEY"
   aws_secret_key: "YOUR_AWS_SECRET_KEY"
   aws_region: "YOUR_AWS_REGION"
   ```
3. **Encrypting `vars/creds.yml`**:
   - Use Ansible Vault to encrypt this file for secure storage and usage.
   - Command to encrypt:
     ```bash
     ansible-vault encrypt vars/creds.yml
     ```
   - You will be prompted to enter a password, which will be required when running Ansible playbooks.

## Creating `vars/main.yml` in Roles
1. **Purpose**: Each role requires a `vars/main.yml` file to define variables specific to the database configuration.
2. **File Locations and Content**:
   - **`db_server/vars/main.yml`**:
     ```yaml
     # db_server/vars/main.yml
     db_name: "employee_db"
     db_user: "db_user"
     db_password: "Passw0rd"
     ```
   - **`web_server/vars/main.yml`**:
     ```yaml
     # web_server/vars/main.yml
     db_server_ip: "{{ hostvars['localhost']['db_server_ip'] }}"
     db_user: "db_user"
     db_password: "Passw0rd"
     db_name: "employee_db"
     ```

3. **Explanation**:
   - `db_server_ip`: Refers to the IP address of the database server.
   - `db_user` and `db_password`: Credentials used to connect to the database.
   - `db_name`: The name of the database being accessed.

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
