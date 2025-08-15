from dataclasses import dataclass


@dataclass
class RSAKeyDTO:
    private_pem: str
    public_pem: str
    n: str
    e: str
