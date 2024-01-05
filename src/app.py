import os
import re
import json
import inquirer
from jira import JIRA
from bardapi import Bard


class Ticket:
    """
    A class used to represent a ticket.

    Attributes
    ----------
    bard_api_key : str
        API token for the Bard model provided by user.
    title : str
        User-provided title of the ticket.
    priority: str
        Ticket priority assigned by the user.
    ticket_body: str
        Final text of the ticket.

    Methods
    -------
    bard_model() -> Bard
        Returns an instance of the language model (Bard).

    clean_description(response: str) -> str
       Returns a cleaned response for describe section by removing unnecessary text generated by Bard.

    get_dict_from_string(text: str) -> dict
        Extracts a dictionary from a string generated by Bard. 
    
    transform_to_string(text_dict: dict) -> str
        Returns a numbered list from the content of the dict

    get_section_text(model:Bard, prompt:str) -> str: 
        Generates text from Bard based on a given prompt. 

    generate_response() -> dict
        Calls using get_section_text() to get all sections of the ticket, returning all text sections in a dictionary.

    create_ticket_body_text() -> str
        Calls generate_response() and concatenates the text sections into a single text.

    get_ticket_priority() -> None
        Provides the user with ticket priority options in the terminal and saves the response.

    upload_ticket_to_jira() -> None
        Creates and uploads the ticket in Jira
    """

    def __init__(self, bard_api_key: str, ticket_title: str):
        self.bard_api_key = bard_api_key
        self.title = ticket_title
        self.priority = None
        self.ticket_body = None

    def bard_model(self):
        """
        Returns an instance of the language model (Bard).
        """
        return Bard(token=self.bard_api_key)

    @staticmethod
    def clean_description(response: str) -> str:
        """
        Returns a cleaned response for describe section by removing unnecessary text generated by Bard.

        Parameters
        ----------
        response : str
            Text generated by Bard

        Returns
        -------
        cleaned_text: str
        """
        # remove text before 'Description'
        result = re.search(r"Description:(.*)", response)
        if result:
            cleaned_text = result.group(1).strip()
            return cleaned_text

        return ""

    @staticmethod
    def get_dict_from_string(response:str) -> dict:
        """
        Extracts a dictionary from a string generated by Bard. 
        Returns an empty dictionary if generated text from Bard is in the wrong format to create a dictionary 

        Parameters
        ----------
        response : str
            Text generated by Bard

        Returns
        -------
        result_dict: dict
        """
        try:
            match = re.search(r'\{.*\}', response, re.DOTALL).group()
            result_dict = json.loads(match)
            return result_dict
        except (AttributeError, json.JSONDecodeError):
            return {}


    @staticmethod
    def transform_to_string(text_dict: dict) -> str:
        """
        Returns a numbered list from the content of the dict

        Parameters
        ----------
        text_dict : dict
            The dict that contains the response of Bard

        Returns
        -------
        section_text: str
            A numbered list of the content for a section in the ticket
        """
        section_text = ""

        for num, (title, text) in enumerate(text_dict.items(), start=1):
            section_text += f"{num}. *{title}*: {text}\n"

        # Remove trailing whitespaces
        section_text = section_text.rstrip()

        return section_text

    def get_section_text(self, model, prompt:str) -> str: 
        """
        Generates text from Bard based on a given prompt. 
        Continues generating responses until a valid dictionary can be extracted from Bard's output.
        
        Parameters
        ----------
        model : Bard
            Instance of Bard
        prompt: str 
            Prompt provided to Bard 

        Returns
        -------
        clean_section_text: str
        """
        
        bard_text = model.get_answer(prompt)["content"]
        bard_dict = self.get_dict_from_string(bard_text)
        
        while bard_dict == {}:
            prompt_adjust = f"fix this dictionary {str(bard_dict)} to match the format {{'key_1' : 'value_1', 'key_2': 'value_2', ..}}"
            bard_text = model.get_answer(prompt_adjust)["content"]
            print(bard_text)
            bard_dict = self.get_dict_from_string(bard_text)

        clean_section_text = self.transform_to_string(bard_dict)

        return clean_section_text

    def generate_response(self) -> dict:
        """
        Uses the Bard model to generate all text sections of the ticket

        Parameters
        ----------
        None

        Returns
        -------
        text_section: dict
            Dictionary which contains the text sections of the ticket
        """
        
        print("Generating Ticket. Please wait...")
        model = self.bard_model()

        # Prompt for description
        prompt_description = f"""
        Only provode a one-line description for the Jira Ticket titled '{self.title}'.

        Description in the following format: 'Description: We need to [TASK] from [RESOURCE] in order for [USER] to [ACTION]'.

        Examples:
        1. Description: We need a modal to assist users in renaming and describing a policy.
        2. Description: We want to establish distinct alarms for production and staging for 'cust-data-classifier' so that developers can identify the environment and respond to issues accordingly.
        """

        description_text = model.get_answer(prompt_description)["content"]
        description_text_clean = self.clean_description(description_text)

        # Prompt for acceptance criteria
        prompt_acceptance_criteria = f"""Given the Jira Ticket titled '{self.title}', provide a structured response in the form of a dictionary containing the acceptance criteria. 
        Emphasize the goals and functionality outlined in the following description: '{description_text_clean}'.

        The return must be a single dictionary where the key is a short title and the value is a single line description, following the format illustrated below:
        ```json
        {{
            Button Placement: The social media sharing button should be prominently placed within the blog post section, preferably near the post title or at the end of the post.,
            Supported Platforms: The button should support sharing on popular social media platforms, including but not limited to Facebook, Twitter, and LinkedIn.,
            Visual Design: The button's design should be consistent with the overall aesthetics of the website. Hover effects should be implemented for a better user experience.
        }}
        ```json
        """
        print("ac section ...")
        acceptance_criteria_text_clean = self.get_section_text(model, prompt_acceptance_criteria)

        # Prompt for subtasks
        prompt_subtasks = f"""Given the Jira Ticket titled '{self.title}', its description {description_text_clean} and acceptance criteria {acceptance_criteria_text_clean}, 
        return a dictionary comprising a concise list of independent subtasks to complete the ticket. 
        Each subtask must be self-contained and mutually exclusive.

        The return must be a single dictionary where the key is a short title and the value is a single line description, following the format as example below:
        ```json
        {{
            Implementation of Button Component: Create a reusable component for the social media sharing button.,
            Integration with Social Media APIs: Integrate the button with the APIs of selected social media platforms for sharing functionality.,
            Styling and Responsiveness: Apply consistent styling to the button and ensure it looks good on all devices.
        }}
        ```json
        """
        print("st section ...")
        subtasks_text_clean = self.get_section_text(model, prompt_subtasks)

    
        # Prompt for assumptions
        prompt_assumptions = f"""Given the Jira Ticket titled '{self.title}', its description {description_text_clean} and acceptance criteria {acceptance_criteria_text_clean}, and with subtasks '{subtasks_text_clean}' 
        return a dictionary comprising a concise list of the assumptions. 

        The return must be a single dictionary where the key is a short title and the value is a single line description, following the example below:
        ```json
        {{
            Backend Support: It is assumed that the backend infrastructure already supports generating shareable links for blog posts,
            API Availability: The availability and stability of the social media platform APIs are assumed for the sharing functionality,
            Design Assets: Necessary design assets, such as icons for social media platforms, are assumed to be available for implementation
        }}
        ```json
        """
        print("as section ...")
        assumptions_text_clean = self.get_section_text(model, prompt_assumptions)


        text_section = {
            "description": description_text_clean,
            "acceptance_criteria": acceptance_criteria_text_clean,
            "subtasks": subtasks_text_clean,
            "assumptions": assumptions_text_clean,
        }

        return text_section

    def create_ticket_body_text(self) -> None:
        """
        Calls generate_response() and concatenates the text sections which is saved as the attribute ticket_body.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # get the text sections for the ticket
        ticket_text_sections = self.generate_response()

        self.ticket_body = f"""

            h2. Task Scope:
            {{panel:bgColor=#deebff}}
            {ticket_text_sections['description']}
            {{panel}}

            h2. Importance/Urgancy:
            {{panel:bgColor=#fefae6}}
            {'Priority: ' + self.priority}
            {{panel}}

            h2. Acceptance Criteria:
            {ticket_text_sections['acceptance_criteria']}

            h2. Sub-tasks:
            {ticket_text_sections['subtasks']}

            h2. Assumptions: 
            {ticket_text_sections['assumptions']}

            """

    def get_ticket_prority(self) -> None:
        """
        Provides the user with ticket priority options in the terminal, and saves the user response as the attribute priority

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        questions = [
            inquirer.List(
                "priority",
                message="Assign a priority to the ticket",
                choices=["Highest", "High", "Medium", "Low", "Lowest"],
            ),
        ]
        answers = inquirer.prompt(questions)
        self.priority = answers["priority"]

    def upload_ticket_to_jira(self, jira_credentials: dict) -> None:
        """
        Create a new ticket in Jira with the content generated by Bard.

        Parameters
        ----------
        jira_credentials: dict
            A dictionary containing the credentials needed to connect with Jira.
            - server (str): The Jira server URL.
            - email_address (str): User's email address for authentication.
            - token (str): Authentication token for accessing Jira.
            - key (str): Project key for identifying the project in Jira.

        Returns
        -------
        None
        """

        # Connect to Jira using provided credentials
        jira = JIRA(
            options={"server": jira_credentials["server"]},
            basic_auth=(jira_credentials["email_address"], jira_credentials["token"]),
        )

        # Prepare issue data
        issue_dict = {
            "project": {"key": jira_credentials["key"]},
            "summary": f"{self.title}",
            "description": f"{self.ticket_body}",
            "priority": {"name": f"{self.priority}"},
            "issuetype": {"name": "Task"},
        }

        try:
            # Create a new issue in Jira
            jira.create_issue(fields=issue_dict)
            print("The following ticket was successfully created and uploaded to Jira:")
            print(f"{self.ticket_body}")
        except Exception as e:
            # Handle any exceptions that may occur during the Jira issue creation
            print(f"Failed to create Jira issue. Error: {str(e)}")


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


def get_ticket_title() -> str:
    """
    Prompts the user to enter a title for a ticket and checks its validity before returning.

    Parameters
    ----------
    None

    Returns
    -------
    ticket_title: str
        User provided title of the ticket
    """

    # Get ticket title from the user
    ticket_title = input("Enter the title of the ticket: ")
    words_in_title = ticket_title.split()

    # error handling of provided title
    if len(words_in_title) == 1:
        print(
            "The title provided contains only a single word. \nTo improve final ticket quality provide a more descriptive title."
        )
        ticket_title = input("Enter improved ticket title: ")
    elif bool(re.match(r"^\d+$", ticket_title)):
        print(
            "Invalid input, unable to create ticket from a title which only contains digits."
        )
        ticket_title = input("Enter improved ticket title: ")

    return ticket_title


if __name__ == "__main__":
    # get Bard and Jira credentials
    jira_credentials = get_jira_credentials()
    bard_api_key = get_bard_api_key()

    # Get ticket title from the user
    ticket_title = get_ticket_title()

    # generate ticket
    ticket = Ticket(bard_api_key, ticket_title.title())
    ticket.get_ticket_prority()
    ticket.create_ticket_body_text()
    ticket.upload_ticket_to_jira(jira_credentials)
