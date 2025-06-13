from socaity.sdk.replicate.meta import meta_llama_3_8b, meta_llama_3_8b_instruct, meta_llama_3_70b_instruct

from socaity import gather_results

cl_test = [
    meta_llama_3_8b,
    meta_llama_3_8b_instruct,
    meta_llama_3_70b_instruct
]

providers = ["socaity"]
prompt = "Write a poem with 3 sentences why an SDK is so much better than plain web requests."

jobs = {}
def test_llama_models():
    for provider in providers:
        for mdl in cl_test:
            llama3 = mdl(service=provider)
            fj = llama3.chat(prompt=prompt)
            jobs[llama3.service_client.service_name] = fj

        results = gather_results(list(jobs.values()))
        for mdl, job in zip(jobs.keys(), results):
            print(f"\n{mdl} provider {provider} , result: {job.get_result()}")


#cl_code_test = [
#    meta_llama_3_13b_code,
#    meta_llama_3_70b_code_python
#]
#code_prompt = "Write a python script to calculate the factorial of a number."
#
#def test_code_models():
#    for provider in providers:
#        for mdl in cl_test:
#            llama3 = mdl(service=provider)
#            fj = llama3.chat(prompt=code_prompt)
#            jobs[llama3.service_client.service_name] = fj
#
#        results = gather_results(list(jobs.values()))
#        for mdl, job in zip(jobs.keys(), results):
#            print(f"\n{mdl} provider {provider} , result: {job.get_result()}")


if __name__ == "__main__":
    test_llama_models()
    test_code_models()
