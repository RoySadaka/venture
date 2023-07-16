from dataclasses import dataclass

@dataclass
class PackageOutput:
    function_name: str
    function_description: str
    response_text: str          