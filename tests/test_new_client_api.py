
"""
model_name, model_type gonna be optional and are used to better find registered models (with services)
endpoint_specification determines how the thing is requested
For services on localhost, in the init of the class one can change the service url.
The thing is smart enough to change to default values if not provided.
"""
from socaity.core.client.request_param import RequestParam
from socaity.core.service_client import ServiceClientAPI

### METHOD ONE ---> CURRENT NEW IMPLEMENTATION
face2face = ServiceClientAPI(service_url="", endpoint_specification="socaity", model_name="test", model_type="")

@face2face.endpoint(route="api/predict", endpoint_specification="socaity", func_type="pre_process")
def swap_one(source_img: str, target_img: int):
    source_img = RequestParam(name="source_img", val=source_img, method="post")
    target_img = RequestParam(name="target_img", val=target_img, method="post")
    return source_img, target_img

@face2face.prepare_params(route="api/swap_from_reference", func_type="definition_only")
def swap_from_reference_face(face_name: str, source_img: str): pass

@face2face.endpoint_post_process(route="api/swap_from_reference")
def swap_from_reference_post_process(job_result):
    return job_result

@face2face.endpoint(route="api/swap_from_reference")
def swap_from_reference(face_name: str, source_img: str):
    return RequestParam(source_img=source_img, target_img=target_img)


#### New Idea:

# Jede Funktion für einen Client braucht eine preprocess, postprocess funktion.
# Anstatt hier alles in einem Rutsch machen zu wollen, kann man wieder eine Methaebene Rauf gehen.
# Sprich zuvor die clientAPI hatte diese Methoden.
# Und nun die WIRKLICHE API, besteht aus mehreren "clientAPIs".
# Die funktion wie swap_one() ruft dann die entsprechende clientAPI auf.

# Naming Vorschlag:
#   - ClientMethod(besteht aus pre/postprocess)
#   - ServiceClientAPI(besteht aus mehreren ClientMethods)

## Beispiel zur Umsetzung der neuen Idee:
## HMMM???

# f2f = ServiceClientAPI(service_url="", endpoint_specification="socaity", model_name="test", model_type="")
# @f2f.client_method(endpoint_route="api/swap_one")
# class SwapOne:
#     def preprocess()
#     def postprocess()

# @f2f.api
# class face2face:
#    def swap_one(source_img: str, target_img: int) -> img: pass


#### Weiteres Gedankenspiel:
# Dekoratoren können in der Funktion ebenfalls gesetzt werden.
# Est sowas möglich?

# @ServiceClientAPI(service_url="", endpoint_specification="socaity", model_name="test", model_type="")
# class Face2Face:
#   def swap_one(target_img, source_img):
        # @pre_process_result
        # myvars
        # @post_process_result
        # do_something


### Oder:
# Service Interface and implement bast

# @ServiceInterface:
# class IFace2Face:
#      def swap_one_img(target_img, source_img) -> blabla: pass
#      def swap_reference(target_img, source_img) -> blabla: pass

# iF2F = IFace2Face()


#
# @iF2F
# class Face2Face:
#    @iF2F.preprocess(name="swap_one_img")
#    def swap_one_img(target_img, source_img):
#        return params
#    @iF2F.postprocess(swap_one_img)
#    def swap_one_img(request_result):
#        return post_processed_result
#
# @ServiceClientAPI(service_url="", endpoint_specification="socaity", model_name="test", model_type="")













# client




