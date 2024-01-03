FROM python:3.9

ENV PYENV_SHELL=/bin/bash
# google LM (BARD) api token
ENV BARD_API_TOKEN_FILE=../secrets/bard_token.txt 
# jira credentials
ENV JIRA_CREDENTIALS_FILE=../secrets/jira_credentials.json

WORKDIR /src

# Create necessary directories
RUN mkdir -p /secrets

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git && \
    pip install -r requirements.txt

# Install Rust using rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Refresh the current shell
RUN /bin/bash -c "source $HOME/.cargo/env"

# Copy the contents of the current directory 
COPY . .

CMD ["/bin/bash"]