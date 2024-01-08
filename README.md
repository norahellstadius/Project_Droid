# Project Droid
**Author: Nora Hallqvist**

## Description 
This Python program automates Jira ticket creation. Simply provide a title, and the program generates a scoped ticket and uploads it to Jira. 

## Approach 
Utilizing the [Bard](https://bard.google.com/chat) (LLM from Google) API, this program generates ticket content from user-provided titles. Post-processing involves regex filters and iterative refinement, enhancing the output's structure and ensuring a tailored result. 

## Important
For the python program to work you need to ensure that you set up the credentials for both Bard and Jira. This setup is detailed in the Installation section below.

## Video Demo
* [Video Demo](https://youtu.be/riW-bcDoXj0)

## Project structure 

```
├── src
│   ├── app.json
│   ├── docker-shell.sh
│   ├── Dockerfile.json
│   ├── requirements.json
│   ├── ticket.py
├── .gitignore
├── README.md
├── docker-compose.yml
```

* `src/app.py` : This file runs the program which creates the ticket and uploads it to Jira 
* `src/docker-shell.sh` : This script is used to build and launch the container.
* `src/Dockerfile` : This file is used to specify the container image.
* `src/requirements` : This file specify the dependencies for the ticket.py and app.py
* `src/ticket.py` : This file is contains the ticket class.
* `docker-compose.py` : This file is run to start the program. It also mounts the secrets.


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

#### b. Add API token for Bard:

In the 'secrets' folder, create a file named 'bard_token.json' with the following content:

```bash
echo '{
  "api_token": "xxxxx"
}' > bard_token.json
```

Replace "xxxxx" with the API key of Bard found following these steps: 
1. Access the [Bard Chat](https://bard.google.com/chat) 
2. Click on 'Inspect' to open the browser developer tools.
3. Navigate to the 'Application' tab within the developer tools.
3. Under 'Cookies', find and copy the value of "__Secure-1PSID".

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

After adding the credentials, the folder structure should look like the following: 

```
├── secrets
│   ├── bard_token.json
│   ├── jira_credentials.json
├── src
│   ├── app.json
│   ├── docker-shell.sh
│   ├── Dockerfile.json
│   ├── requirements.json
│   ├── ticket.py
├── .gitignore
├── README.md
├── docker-compose.yml
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

This will run the container and automatically execute the Python script, guiding the user to create a ticket from just a title.

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
- Based on the title classify the ticket (ML model) as a specific type (e.g Bug, Task etc.)
- Experiment with better (stronger) LLM models like GPT-4 (I expected it should generated improved content)