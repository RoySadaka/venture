from venture.config import Config


SYSTEM_MESSAGE  = """Your name is Venture.
{}
Your task is to evaluate and judge the outputs produced by various other AI systems.
These other AI systems were provided with a user query and instructions to execute it.
Every other AI system has generated a unique response to this query, accompanied by a function_name that signifies the functionality chosen by the AI.
It's your duty to deeply scrutinize these results and select the one that has shown the utmost efficiency in addressing the specified query.
"""

USER_MESSAGE = """User query:
```
{}
```

AI Inputs and Responses:
```
{}
```

---

Venture, please do not use any knowledge outside the provided information.
Only use the function you have been provided with."""


RESPONSE_WITHOUT_FUNCTION_NAME_HANDLER = {
                    "name" : "response_without_function_name_handler",
                    "description" : "This handler represent AI that decided to return only text response, without picking specific function_name"
                    }


VERDICT_HANDLER = {
                    "name" : "verdict_handler",
                    "description" : "This handler is responsible for providing a final decision or judgment based on the evaluation of the AI systems' outcomes",
                    "parameters" : 
                    {
                        "type": "object",
                        "properties":
                        {
                            "reasoning": 
                            {
                                "type": "string",
                                "description": "Venture's short reasoning why the chosen_function_name is the most relevant to the user's query"
                            },

                            "chosen_function_name": 
                            {
                                "type": "string",
                                "description": "According to your verdict, this function_name has been identified as the most effective in successfully addressing the provided query",
                            }
                        },
                        "required": ["reasoning", "chosen_function_name"]
                    }
                    }