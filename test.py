from socaity import create_client

#### CLIENT API  ####
from socaity import Bark
result = Bark("localhost").run("Hello", affe=2) ## Represents client class subclassing

### Simple API ###
from socaity import text2speech
text2speech("Hello") ## Represents decorator usage

#### Advanced API ####
# create a client
bark_client = create_client(model_name="bark", endpoint_type="localhost")
# create a job
job = text2speech("Hello")
bark_client.run(job)
