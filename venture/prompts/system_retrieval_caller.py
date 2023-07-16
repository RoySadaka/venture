from venture.config import Config


SYSTEM_MESSAGE  = """Your name is Venture.
{}
Your expertise is to make the best decision on which function handler to choose based on user query.
Your response to the user should be helpful, polite, and intelligent.
You are tasked with determining the most appropriate function handler to invoke given the descriptions and details of the functions and based on the user's query.
The chosen function handler will then be used to select a document that contains more comprehensive information about the function.
"""

USER_MESSAGE = """User query:
```
{}
```

---

Venture, please do not use any knowledge outside the provided Knowledge Base.
Only use the functions you have been provided with.
It is mandatory for you to select a function name that has shown the utmost efficiency in addressing the specified query.
"""

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
                        "name" : "unrecognized_query_handler",
                        "description" : "Handles queries that don't appear to be associated with any other specified function call descriptions",
                        "parameters" : 
                        {
                            "type": "object",
                            "properties": 
                            {
                                "response": 
                                {
                                    "type": "string",
                                    "description": "The response from Venture to politely indicate that it doesn't know how to handle the query"
                                }
                            },
                            "required": ["response"]
                        }
                        }

VENTURE_TOPIC_HANDLER = {
                        "name":'venture_topic_handler',
                        "description":f"Handling for queries about Venture's operational environment.\n{Config.VENTURE_UI_DESCRIPTION}",
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
                                "reasoning": 
                                {
                                    "type": "string",
                                    "description": "If this document is deemed the most pertinent to the user's query, a brief explanation will be provided as to why it holds that distinction"
                                }
                            },
                            "required": ["reasoning"]
                        }
                        }