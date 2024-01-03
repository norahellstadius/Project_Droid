FROM python:3.9

ENV PYENV_SHELL=/bin/bash
ENV BARD_API_TOKEN_FILE=../secrets/bard_token.txt 

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

# Copy the contents of the current directory 
COPY . .

CMD ["/bin/bash"]