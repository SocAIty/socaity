from pydantic import BaseModel, Field

class DeepSeekR1_Input(BaseModel):
    prompt: str = Field(default="")
    max_tokens: int = Field(default=20480, gt=0)
    temperature: float = Field(default=0.1, ge=0, le=1)
    presence_penalty: float = Field(default=0.0)
    frequency_penalty: float = Field(default=0.0)
    top_p: float = Field(default=1.0, ge=0, le=1)

