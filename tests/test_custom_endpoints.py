from socaity import ClientAPI, await_result, await_results
from socaity.registry import add_socaity_endpoint

#### Test Socaity Router
add_socaity_endpoint(service_url="http://localhost:8000/", model_name="test", endpoint_name="api/predict")

class testSocaityRouter(ClientAPI):
    def __init__(self):
        super().__init__(model_name="test", endpoint_type="socaity")

    def run(self, my_param1: str, my_param2: int):
        return super().run(my_param1=my_param1, my_param2=my_param2)


job = testSocaityRouter().run("Hello test 1", 2)
r = await_result(job)

tsr = testSocaityRouter()
jobs = [tsr.run(f"Hello {i}", 2) for i in range(10)]
results = await_results(jobs)
a =1