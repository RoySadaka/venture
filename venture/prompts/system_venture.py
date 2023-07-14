from venture.config import Config


SYSTEM_MESSAGE  = f"""Your name is Venture.
{{}}
Your expertise is to read project documentations (referred to as Knowledge Base), and try to find an answer to a user query in that Knowledge Base.
Your response to the user should be helpful, polite, and intelligent.

{Config.VENTURE_UI_DESCRIPTION}

The user is currently at the Explore Tab.

---

Knowledge Base:
{{}}
"""

USER_REMINDER = """\n---\nVenture, please do not use any knowledge outside the provided Knowledge Base.
Only use the functions you have been provided with.
It is mandatory for you to select one of the available functions."""


MISSING_ANSWER_HANDLER = {
                            "name":"missing_answer_in_knowledge_base_handler",
                            "description":"Utilize this handler when the user's inquiry cannot be answered by the information available in the provided knowledge base.",
                            "parameters":
                            {
                                "type": "object",
                                    "properties": 
                                    {
                                        "response": 
                                        {
                                            "type": "string",
                                            "description": "If answer is missing, represents Venture's response for the user, saying that no answer was found in Knowledge Base.",
                                        },
                                    },
                                    "required": ["response"]
                            }
                            }

ANSWER_FOUND_HANDLER = {
                        "name":"found_answer_in_knowledge_base_handler",
                        "description":"Utilize this handler when the answer to the user's query is discovered within the provided Knowledge Base.",
                        "parameters":
                        {
                            "type": "object",
                            "properties": 
                            {
                                "response": 
                                {
                                    "type": "string",
                                    "description": "If answer found, represents Venture's response for the user's query based on the Knowledge Base",
                                },
                            },
                            "required": ["response"]
                        }
                        }

ALL_FUNCTIONS = [ANSWER_FOUND_HANDLER, MISSING_ANSWER_HANDLER]
