from abc import abstractmethod

class _BaseChat:
    @abstractmethod
    def chat(self, prompt: str, *args, **kwargs) -> str:
        """
        Prompts an LLM.
        :param text: The text to prompt the LLM with.
        :return: The generated response from the llm.
        """
        raise NotImplementedError("Please implement this method")


# Factory method for generalized model_hosting_info calling
def chat(prompt: str, model="meta-llama-3-13b", service="socaity", *args, **kwargs) -> str:
    from .llama3 import MetaLLama3_70b, MetaLLama3_8b, MetaLLama3_70b_code_python, MetaLLama3_13b_code, MetaLLama3_70b_instruct
    from .deepseek import DeepSeekR1
    names_cl = {
        "meta-llama-3-8b": MetaLLama3_8b,
        "meta-llama-3-70b": MetaLLama3_70b,
        "meta-llama-3-70b-code": MetaLLama3_70b_code_python,
        "meta-llama-3-13b-code": MetaLLama3_13b_code,
        "meta-llama-3-70b-instruct": MetaLLama3_70b_instruct,
        "deepseek-r1": DeepSeekR1
    }
    names_cl = {k.lower().replace("-", ""): v for k, v in names_cl.items()}
    mdlcl = names_cl.get(model.lower().replace("-", ""), MetaLLama3_8b)

    return mdlcl(service=service).chat(prompt=prompt, *args, **kwargs)
