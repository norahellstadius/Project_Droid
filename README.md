# Project Droid
**Author: Nora Hallqvist**

## Video Demo
* [Video Demo]()

## Installation 

### 1. Clone the Repository

```bash
git clone git@github.com:norahellstadius/Project_Droid.git
```

### 2. Add Credentials

After cloning the repository, follow these steps to add the necessary credentials for Bard (LLM model) and Jira:

#### a. Create a 'secrets' folder

On the same level as 'src', create a folder called 'secrets'

```bash
mkdir secrets
cd secrets
```

After adding the credentials, the folder structure should look like the following: 

```
├── secrets
│   ├── bard_token.json
│   ├── jira_credentials.json
├── src
│   ├── docker-shell.sh
│   ├── Dockerfile.json
│   ├── requirements.json
│   ├── test.json
├── docker-compose.yml
├── README.md
```

#### b. Add API token for Bard:

In the 'secrets' folder, create a file named 'bard_token.json' with the following content:

```bash
echo '{
  "api_token": "xxxxx"
}' > bard_token.json
```

#### c. Add credentials for Jira

In the 'secrets' folder, create a file named 'jira_credentials.json' with the following content:

```bash
echo '{
  "server": "https://server_name.atlassian.net",
  "email_address": "workspace_email@gmail.com",
  "token": "xxxxxx",
  "key": "project_key_name"
}' > jira_credentials.json
```

### 3. Build the Docker Image

Navigate to the 'src' directory and build the Docker image by running the command:

```bash
sh docker-shell.sh
```



## Getting Started 

### 1. Run the Container

To run the container, use Docker Compose, which mounts the secrets (credentials for Bard and Jira). Navigate out of 'src' and run the command:

```bash
docker-compose run app
```

This will run the container and automatically execute the Python script, guiding the user to create a ticket from just a title).

### 2. Create a Ticket

#### a. Provide a ticket title 

In the terminal, the user is prompted with:

```bash
Enter the title of the ticket:
```

The user should enter the title and press enter. For example:

```bash
Enter the title of the ticket: Add Social Media Sharing Buttons to Blog Posts
```

*Note: if the user only provides a single word or only digits the user is asked to provide an improved title.* 

#### b. Provide a priority status of ticket

After providing a sufficient title the user is prompted with an option to choose the priority of the ticket. 

```bash
[?] Assign a priority to the ticket?: Highest
    > Highest
    High
    Medium
    Low
    Lowest
```

#### c. Final Ticket
This initiates the generation of the ticket and if the credentials of Jira are successfully set up, the fully scoped ticket should be uploaded under the project in Jira. The ticket content is also printed in the terminal.

## Future Work 
- Fine-tune an LLM model with training pairs including titles and well-scoped tickets as the input and label, respectively.
