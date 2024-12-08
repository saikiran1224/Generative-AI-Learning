from pydantic import BaseModel

# data class to map the input values
class BankNote(BaseModel):

    variance: float
    skewness: float
    curtosis: float
    entropy: float