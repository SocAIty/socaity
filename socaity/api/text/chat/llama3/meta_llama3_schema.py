from pydantic import BaseModel, Field


class _MetaLlama3_common(BaseModel):
    prompt: str = Field(default="")
    temperature: float = Field(default=0.6, ge=0, le=1)
    top_p: float = Field(default=0.9, ge=0, le=1)
    frequency_penalty: float = Field(default=0.2)
    presence_penalty: float = Field(default=1.15)

class MetaLlama3_Input(_MetaLlama3_common):
    max_tokens: int = Field(default=512, gt=0)
    length_penalty: float = Field(default=1.0, ge=0, le=5)
    prompt_template: str = Field(default="{prompt}")
    seed: int = Field(default=0, ge=0)

class MetaCodeLlama3_Input(_MetaLlama3_common):
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
    prompt_template: str = Field(
        default="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        You are a helpful assistant<|eot_id|><|start_header_id|>user<|end_header_id|>
        {prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """
    )
