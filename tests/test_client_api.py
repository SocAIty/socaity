from socaity import create_client, ClientAPI, await_result
from socaity.socaity_client import EndPoint
from socaity.registry import add_socaity_endpoint
#### CLIENT API  ####
from socaity import Bark, await_results

# test of async
job = Bark("localhost").run("Hello") ## Represents client class subclassing
result = await_result(job)

b = Bark("localhost")
async_jobs = [b.run(f"Hello {i}", somerandomarg=2) for i in range(20)]
results = await_results(async_jobs)

# test of sync methods
job2 = Bark("localhost").run_sync("Hello2", affe=2) ## Represents client class subclassing
audio, sample_rate = job.result

