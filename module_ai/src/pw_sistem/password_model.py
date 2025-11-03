from pydantic import BaseModel

class PasswordGenerate(BaseModel):
    length: int
    include_capital: bool
    include_lower: bool
    include_number: bool
    include_symbols: bool

class PassphraseGenerate(BaseModel):
    words_number: int
    separator: str
    include_number: bool
    include_symbol: bool
    capitalize: bool
    english: bool
    spanish: bool

class PasswordRequest(BaseModel):
    password_id: int
    master_password: str = ""
