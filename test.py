from socaity.registry.jobs import text2speech
from socaity.core.ClientFactory import create_client

#### THIS IST THE WAY TO GO #####
# create a client
bark_client = create_client(model_name="bark", endpoint_type="localhost")
# create a job
job = text2speech("Hello")
bark_client.run(job)


#### BY USING THE API CLASS WE CAN SIMPLIFY THE USAGE ####
from socaity.api import bark, text2speech
bark().run("Hello")
text2speech("Hello")
