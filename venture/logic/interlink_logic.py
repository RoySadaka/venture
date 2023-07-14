from venture.objects.interlink_commander_details_output import InterlinkCaptainDetailsOutput
from venture.metadata import Metadata
from venture.config import Config
import webbrowser

def get_interlink_message(metadata:Metadata, user_query:str) -> str:
    response_text = metadata.explore_llm_output.response_text
    return f"""Hey Captain,
Venture was unable to find a satisfactory answer to my query. 
I would greatly appreciate it if you could assist me in finding the information I need.
    
My Query:
```
{user_query}
```

Venture's Response:
```
{response_text}
```

Thank you for your attention to this matter. 
I look forward to your assistance. 
Please feel free to contact me if you require any additional information.

Best regards"""

def get_captain_details_textbox_visibility(metadata:Metadata):
    return metadata.interlink_captain_details.has_contact_details or metadata.interlink_captain_details.has_email_address

def get_captain_details_textbox_text(metadata:Metadata):
    return metadata.interlink_captain_details.contact_details \
                    if metadata.interlink_captain_details.has_contact_details \
                    else metadata.interlink_captain_details.email_address

def invoke_email_draft(metadata:Metadata, body:str):
    subject = 'Venture Inquiry - documentation question'
    body = body.replace('\\',',')
    if metadata.interlink_captain_details.has_email_address:
        webbrowser.open(f'mailto:{metadata.interlink_captain_details.email_address}?subject={subject}&body={body}')
    else:
        webbrowser.open(f'mailto:?subject={subject}&body={body}')

def update_interlink_captain_details(metadata:Metadata):
    all_contact_details = []
    if metadata.explore_llm_output is not None:
        for used_context_file_name in metadata.explore_llm_output.used_context_file_names:
            if used_context_file_name not in metadata.file_name_to_parsed_doc:
                continue
            contact_details = metadata.file_name_to_parsed_doc[used_context_file_name].contact_details
            if contact_details is not None:
                all_contact_details.append(contact_details)
    if len(all_contact_details) == 0:
        metadata.interlink_captain_details = InterlinkCaptainDetailsOutput(contact_details=None, email_address=Config.CAPTAIN_EMAIL)
    else:
        metadata.interlink_captain_details = InterlinkCaptainDetailsOutput(contact_details='\n---\n'.join(all_contact_details), email_address=None)