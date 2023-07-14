SYSTEM_MESSAGE = """Review the project documentation to search for owner's name and/or contact email address."""

USER_REMINDER = """\n---\nPlease do not use any knowledge outside the provided documentation.
Only use the functions you have been provided with.
It is mandatory for you to select one of the available functions."""


EXPLICIT_CONTACTS_DETAILS = 'explicit_contacts_details'

OWNERSHIP_HANDLER = {
                    "name":"contact_details_in_documentation_handler",
                    "description":"Project owners or contact persons that are explicitly and implicitly written in provided documentation",
                    "parameters": 
                    {
                        "type": "object",
                        "properties":
                        {
                            EXPLICIT_CONTACTS_DETAILS: 
                            {
                                "type": "array",
                                "items": 
                                {
                                    "type": "string",
                                    "description": "Explicit project owner name or contact email address written in provided documentation"
                                },
                            },
                        },
                    }
                    }