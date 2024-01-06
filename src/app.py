import os
import re
import json
from ticket import Ticket

def get_bard_api_key() -> str:
    """
    Get the api tokens for the LLM model (Bard).

    Parameters
    ----------
    None

    Returns
    -------
    api_token_dict: str
    """

    file_path = os.getenv("BARD_API_TOKEN_FILE")

    try:
        with open(file_path, "r") as file:
            api_token = json.load(file)

        return api_token["api_token"]

    except Exception as e:
        print(f"Error reading API token file: {e}")
        raise RuntimeError("Failed to read API token file")


def get_jira_credentials() -> dict:
    """
    Get credentials for Jira.

    Parameters
    ----------
    None

    Returns
    -------
    jira_credentials: dict
        A dictionary containing the credentials needed to connect with Jira.
        - server (str): The Jira server URL.
        - email_address (str): User's email address for authentication.
        - token (str): Authentication token for accessing Jira.
        - key (str): Project key for identifying the project in Jira.
    """

    file_path = os.getenv("JIRA_CREDENTIALS_FILE")

    try:
        with open(file_path, "r") as file:
            credentials = json.load(file)
        return credentials

    except Exception as e:
        print(f"Error reading jira credentials: {e}")
        raise RuntimeError("Failed to read jira credentials")


if __name__ == "__main__":
    # get Bard and Jira credentials
    jira_credentials = get_jira_credentials()
    bard_api_key = get_bard_api_key()

    # generate ticket
    ticket = Ticket(bard_api_key)
    ticket.get_ticket_title()
    ticket.get_ticket_prority()
    ticket.create_ticket_body_text()
    ticket.upload_ticket_to_jira(jira_credentials)
