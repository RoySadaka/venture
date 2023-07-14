from venture.config import Config


SYSTEM_MESSAGE  = """Your name is Venture.
{}
Your expertise is to make the best decision on which function handler to choose based on user query.
Your response to the user should be helpful, polite, and intelligent.
You are tasked with determining the most appropriate function handler to invoke given the descriptions and details of the functions and based on the user's query.
The chosen function handler will then be used to select a document that contains more comprehensive information about the function.
"""

USER_REMINDER = """\n---\nVenture, please do not use any knowledge outside the provided Knowledge Base.
Only use the functions you have been provided with.
It is mandatory for you to select one of the available functions."""

GREETING_HANDLER = {
                    "name" : "greeting_handler",
                    "description" : "Handle user greetings and provide a Venture response if the user only greets without asking anything.",
                    "parameters" : 
                    {
                        "type": "object",
                        "properties":
                        {
                            "response": 
                            {
                                "type": "string",
                                "description": "Venture's response to provide to the User in response to their greeting",
                            }
                        },
                        "required": ["response"]
                    }
                    }

CLARIFICATION_HANDLER = {
                        "name" : "clarification_required_handler",
                        "description" : "Venture will ask for clarification when the query is confusing and it is unclear whether Venture can answer it with a specific documentation",
                        "parameters" :
                        {
                            "type": "object",
                            "properties":
                            {
                                "response": 
                                {
                                    "type": "string",
                                    "description": "Venture's response asking for clarification"
                                }
                            },
                            "required": ["response"]
                        }
                        }

UNKNOWN_TOPIC_HANDLER = {
                        "name" : "unknown_topic_handler",
                        "description" : "Handles unknown topics that are not part of any other provided function call topics",
                        "parameters" : 
                        {
                            "type": "object",
                            "properties": 
                            {
                                "response": 
                                {
                                    "type": "string",
                                    "description": "Venture's response to politely handle the unknown query"
                                }
                            },
                            "required": ["response"]
                        }
                        }

VENTURE_TOPIC_HANDLER = {
                        "name":'venture_topic_handler',
                        "description":Config.VENTURE_UI_DESCRIPTION,
                        "parameters":
                        {
                            "type": "object",
                            "properties": 
                            {
                                "tab": 
                                {
                                    "type": "string",
                                    "description": "The tab name the query ask about, one of ['Explore', 'Cosmos', 'Interlink']"
                                },
                                "response": 
                                {
                                    "type": "string",
                                    "description": "Venture's response to Venture abilities query"
                                }
                            },
                            "required": ["response"]
                        }
                        }

NON_TEMPLATE_FUNCTIONS = [GREETING_HANDLER, CLARIFICATION_HANDLER, UNKNOWN_TOPIC_HANDLER, VENTURE_TOPIC_HANDLER]

NON_TEMPLATE_HANDLER_NAMES = {f['name'] for f in NON_TEMPLATE_FUNCTIONS}

TEMPLATE_TOPIC_HANDLER = {
                        "name":"{}",
                        "description":"Handles queries related to:\n{}",
                        "parameters": 
                        {
                            "type": "object",
                            "properties": 
                            {
                                "response": 
                                {
                                    "type": "string",
                                    "description": "Venture's response that will indicate that the system will handle the query via the chosen handler"
                                }
                            },
                            "required": ["response"]
                        }
                        }