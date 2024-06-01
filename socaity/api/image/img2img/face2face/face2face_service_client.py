import time

from socaity.core.definitions.enums import EndpointSpecification, ModelDomainTag, ModelTag
from socaity.core.web.service_client import ServiceClient


srvc_face2face = ServiceClient(
    service_url="localhost:8000/api",
    model_name="face2face",
    model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO],
    model_tags=[ModelTag.FACE2FACE, ModelTag.IMAGE2IMAGE]
)

srvc_face2face.add_endpoint(endpoint_route="swap_from_reference")
srvc_face2face.add_endpoint(endpoint_route="/swap_one", post_params={"source_img": str, "target_img": str})
srvc_face2face.add_endpoint(endpoint_route="status")
srvc_face2face.add_endpoint(endpoint_route="kartoffel", post_params={"mach_pommes": str})

if __name__ == "__main__":
    srvc_face2face.list_endpoints()
    request = srvc_face2face.kartoffel_async(mach_pommes="kartoffel start")

    while True:
        time.sleep(105)
        a = 1


    #jobs = {str(i): srvc_face2face.kartoffel_async(mach_pommes=f"kartoffel {i}") for i in range(20)}
#
    #finished_jobs = []
#
    #while len(finished_jobs) < len(jobs):
    #    for i, job in jobs.items():
    #        if i not in finished_jobs and job._state == "FINISHED":
    #            finished_jobs.append(i)
    #            print(job.result)




    req = srvc_face2face.kartoffel_async("kartoffel2")
    #req = srvc_face2face.swap_one(source_img="source.jpg", target_img="target.jpg")
    #req_async = srvc_face2face.swap_one_async("source.jpg", "target.jpg")
    #req_async = srvc_face2face("swap_one", "source.jpg", "target.jpg")
