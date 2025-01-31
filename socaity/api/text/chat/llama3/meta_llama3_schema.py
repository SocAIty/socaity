from pydantic import BaseModel, Field

class MetaLlama3_Input(BaseModel):
    prompt: str = Field(default="")
    max_tokens: int = Field(default=512, gt=0)
    temperature: float = Field(default=0.6, ge=0, le=1)
    top_p: float = Field(default=0.9, ge=0, le=1)
    presence_penalty: float = Field(default=1.15)
    frequency_penalty: float = Field(default=0.2)

class MetaCodeLlama3_Input(MetaLlama3_Input):
    repeat_penalty: float = Field(default=1.0, ge=0, le=2)


class MetaLlama3_InstructInput(BaseModel):
    prompt: str = Field(default="")
    system_prompt: str = Field(default="You are a helpful assistant")
    max_new_tokens: int = Field(default=512, gt=0)
    temperature: float = Field(default=0.6, ge=0, le=1)
    top_p: float = Field(default=0.9, ge=0, le=1)
    length_penalty: float = Field(default=1.0)
    stop_sequences: str = Field(default="<|end_of_text|>,<|eot_id|>")
    presence_penalty: float = Field(default=0.0)
    frequency_penalty: float = Field(default=0.2)
