SYSTEM_MESSAGE  = f"""Your role is to generate file names for project documentation based on project summaries.
Your objective is to read the summary and generate a concise file name consisting of 1 to 3 words that effectively captures the core concept of the project based on the provided summary"""

USER_MESSAGE_TEMPLATE = 'Project Summary:\n\n```\n{}\n```'

FILE_NAME_HANDLER = {
                        "name":"file_name_handler",
                        "description":"A function that will save to file to disk with the given file name",
                        "parameters":
                        {
                            "type": "object",
                            "properties": 
                            {
                                "file_name": 
                                {
                                    "type": "string",
                                    "description": "A concise file name consisting of 1 to 3 words that effectively captures the core concept of the project based on the provided summary",
                                },
                            },
                            "required": ["file_name"]
                        }
                        }

