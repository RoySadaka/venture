SYSTEM_MESSAGE = """Examine the project documentation thoroughly, identifying any instances where the owner's name and/or contact email address are mentioned.
This could require detecting references to terms like 'owner', 'leader', 'project lead', 'contact person', or any other indirectly expressed terms that could imply the presence of a contact individual."""

USER_MESSAGE = """Project documentation:
```
{}
```

---

Please do not use any knowledge outside the provided documentation.
Only use the functions you have been provided with.
It is mandatory for you to select one of the available functions."""


EXPLICIT_CONTACTS_DETAILS = 'contacts_details'

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
                                    "description": "Representing project owner name or contact email address written in provided documentation"
                                },
                            },
                        },
                    }
                    }