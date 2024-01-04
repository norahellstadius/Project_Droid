FROM python:3.9

ENV PYENV_SHELL=/bin/bash
# google LM (BARD) api token
ENV BARD_API_TOKEN_FILE=../secrets/bard_token.json 
# jira credentials
ENV JIRA_CREDENTIALS_FILE=../secrets/jira_credentials.json

#set working directory
WORKDIR /src

# Create necessary directories
RUN mkdir -p /secrets

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Install Rust using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Refresh the current shell for Rust 
RUN /bin/bash -c "source $HOME/.cargo/env"

# Copy the contents of the current directory 
COPY . .

#run app script when container is run
CMD ["python", "app.py"]