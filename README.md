# Preliminary Steps

## 1. Clone the Repository

```bash
git clone git@github.com:norahellstadius/Project_Droid.git
```

## 2. Add Credentials

After cloning the repository, follow these steps to add necessary credentials:

### a. Create a 'secrets' folder

```bash
mkdir secrets
cd secrets
```

### b. Add api token for the Bard:

In the 'secrets' folder, create a file named 'bard_token.json' with the following content:

```bash
echo '{
  "api_token": "xxxxx"
}' > bard_token.json
```

### c. Add credentials for Jira

In the 'secrets' folder, create a file named 'jira_credentials.json' with the following content:

```bash
echo '{
  "server": "https://server_name.atlassian.net",
  "email_address": "workspace_email@gmail.com",
  "token": "xxxxxx",
  "key": "project_key_name"
}' > jira_credentials.json
```

# Project Organization

After adding the credentials, the project should follow this structure:

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

## Getting Started 

1. **Build the Docker Image**

   Navigate to the 'src' directory and build the Docker image by running the command:

   ```bash
   sh docker-shell.sh
   ```

2. **Run the Container**

   To run the container, use Docker Compose, which mounts the secrets (credentials for Bard and Jira). To accomplish this navigate out of 'src' and run the command:

   ```bash
   docker-compose run app
   ```

   This will run the container and automatically execute the Python script, guiding the user to create a ticket from a minimally described task (with just a title).

3. **Create a Ticket**

   In the terminal, the user is prompted with:

   ```bash
   Enter the title of the ticket:
   ```

   The user should enter the title and press enter. For example:

   ```bash
   Enter the title of the ticket: create blue button
   ```

   This initiates the process of creating a ticket based on the provided title.

  
TODO: 
- add comments to code 
- in readme describe the credentials beter like what is service_account 
- improve formate and spacing using librarys 
- create checklist for the acceptance criteria



Future work 
- finetune the LLM with sample Jira tickets with training pairs i.e titles and well scoped ticket as the label and input respectively. 

