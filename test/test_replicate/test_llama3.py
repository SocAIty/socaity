import os
from socaity.sdk.replicate.meta import meta_llama_3_8b, meta_llama_3_8b_instruct, meta_llama_3_70b_instruct
from fastsdk import gather_results

cl_test = [
    meta_llama_3_8b,
    meta_llama_3_8b_instruct,
    meta_llama_3_70b_instruct
]

prompt = "Write a poem with 3 sentences why an SDK is so much better than plain web requests."


def test_llama_models():
    jobs = {}
    for mdl in cl_test:
        llama3 = mdl(api_key=os.getenv("SOCAITY_API_KEY", None))
        fj = llama3(prompt=prompt)
        jobs[llama3.service_definition.display_name] = fj

    results = gather_results(list(jobs.values()))
    for mdl, job in zip(jobs.keys(), results):
        print(f"\n{mdl} result: {job.get_result()}")
    return results


if __name__ == "__main__":
    test_llama_models()
