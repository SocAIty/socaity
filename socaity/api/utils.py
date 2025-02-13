from fastsdk.utils import get_function_parameters_as_dict


def get_model_instance(
        name_instance_dict: dict,
        model_name: str,
        service: str = "socaity",
        default_instance=None):
    # get model class from name_instance_dict
    names_cl = {k.lower().replace("-", ""): v for k, v in name_instance_dict.items()}
    if not default_instance:
        default_instance = list(name_instance_dict.values())[0]

    # instantiate class
    mdlcl = names_cl.get(model_name.lower().replace("-", ""), default_instance)
    return mdlcl(service=service)


def execute_job_function(job_func: callable, pam_locals: dict):
    pams = get_function_parameters_as_dict(job_func,exclude_param_names="job", func_kwargs=pam_locals)
    return job_func(**pams)
