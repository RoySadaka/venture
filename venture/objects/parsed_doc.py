from dataclasses import dataclass


@dataclass
class ParsedDoc:
    file_name: str
    function_name: str
    content: str
    content_token_count: int
    hash: str
    summary: str
    summary_token_count: int
    contact_details: str

    def to_json(self):
        return {
                'file_name':self.file_name,
                'function_name':self.function_name,
                'content':self.content,
                'content_token_count':self.content_token_count,
                'hash':self.hash,
                'summary':self.summary,
                'summary_token_count':self.summary_token_count,
                'contact_details':self.contact_details
                }

    @staticmethod
    def from_json(json_str):
        return ParsedDoc(file_name=json_str['file_name'],
                         function_name=json_str['function_name'],
                         content=json_str['content'],
                         content_token_count=json_str['content_token_count'],
                         hash=json_str['hash'],
                         summary=json_str['summary'],
                         summary_token_count=json_str['summary_token_count'],
                         contact_details=json_str.get('contact_details',None))