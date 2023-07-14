from dataclasses import dataclass


@dataclass
class InterlinkCaptainDetailsOutput:
    contact_details: str
    email_address: str

    @property
    def has_contact_details(self) -> bool:
        return self.contact_details is not None and len(self.contact_details.strip()) > 0
    
    @property
    def has_email_address(self) -> bool:
        return self.email_address is not None and len(self.email_address.strip()) > 0