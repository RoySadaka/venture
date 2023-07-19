class Config:
    # LOGIC
    MIN_TOKENS_TO_CONSIDER_DOC = 200
    MAX_TOKENS_TO_CONSIDER_DOC = 14_000
    FUNCTION_CALL_ADDED_TOKEN_COUNT = 11
    RESERVED_RETRIEVAL_TOKEN_COUNT = 500
    RESERVED_RESPONSE_TOKEN_COUNT = 1000
    SUMMARY_RESERVED_RESPONSE_TOKEN_COUNT = 1000
    OWNERSHIP_RESERVED_RESPONSE_TOKEN_COUNT = 200
    FUNCTION_NAME_RESERVED_RESPONSE_TOKEN_COUNT = 200
    ERROR_RESPONSE = "Apologies, there seems to be an unknown error.\nPlease try again or contact the devs."
    MODEL_NAME_TO_MAX_TOKENS = {'gpt-3.5-turbo-0613':4096, 'gpt-3.5-turbo-16k-0613':16384}
    MODEL_NAME_TO_COST_PER_TOKEN = {'gpt-3.5-turbo-0613':{'in':0.0000015,'out':0.000002}, 'gpt-3.5-turbo-16k-0613':{'in':0.000003,'out':0.000004}}
    MODEL_NAME_16K = 'gpt-3.5-turbo-16k-0613'
    TOKENIZER_NAME = 'cl100k_base'
    OPEN_AI_FUNCTION_MAX_LENGTH = 64
    OPEN_AI_FUNCTION_TEMPLATE_SUFFIX = '_handler'
    IRRELEVANT_PROJECT_OWNERS = {'owner', 'leader', 'project lead', 'contact person'}

    CAPTAIN_EMAIL = ''
    EXTRA_ROLE = ''
    OPEN_AI_KEY = ''

    # UI
    MAX_DOCS_TO_USE_AS_CONTEXT  = 2
    AUTO_PILOT_NAME             = "Auto-Pilot"
    CASUAL_DETAILS_TEMPLATE     = '<br><br><br><br><br><sub><sup><span style="color:black">{}</span></sup></sub>'

    # FILES
    DATA_PATH                   = './venture/cosmos_data/'
    PARSED_FILES_PATH           = './parsed_files/'
    INDEX_PATH                  = './index/'

    # PROMPTS
    VENTURE_UI_DESCRIPTION = """Venture, Your operational environment is a User Interface (UI) that is segmented into the following tabs:
1. Explore Tab: This tab users will interact with you to inquire about project documentation. They have the option to request for specific documentation, or to use the 'Auto-Pilot' feature which autonomously provides them with the required documentation.
2. Cosmos Tab: This tab dedicated to the management of the documentations. Users are allowed to add new project documentation and also have the capability to remove any existing documentations.
3. Interlink Tab: This tab serves as a communication channel between users and the support team. If a user encounters any ambiguity or finds that a documentation needs an update, they can utilize this tab to reach out to the support team for assistance."""