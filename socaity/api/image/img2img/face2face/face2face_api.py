from socaity.core.jobs.threaded.job_manager import JobManager
from socaity.api.image.img2img.face2face.face2face_service_client import srvc_face2face
import cv2


# this adds a request function to the service client.
# The request function then is used within the methods.
#   Using this approach I know when the server is called and from which function.
#   Thus it can be added to the same "internal_job"
@ServiceClientAPI("service_name")
class face2face:

    # This creates an "internal_job" object. The job is added to the job manager and processed threaded.
    #   once a request is send, this is known also and the job state changes.
    @ServiceClientAPI.job
    def swap_one_from_file(self, source_img: str, target_img: str, job_progress) -> img:
        source_img = cv2.imread(source_img)
        target_img = cv2.imread(target_img)
        job_progress.message = "started"

        # here the wrapper must be so smart, that it will not create a second job instance
        # but it must pass the job_progress object to the already existing job instance
        return self.swap_one(source_img, target_img)

    @ServiceClientAPI.job
    def swap_one(self, source_img: np.array, target_img: np.array, job_progress) -> np.array:
        # method to call it "sync"
        request_result = srvc_face2face.swap_one(source_img, target_img)
        # method to call it "async_jobs"
        web_service_async_io_task = srvc_face2face.swap_one_async(source_img, target_img)
        # use async_jobs way to for example make status updates
        while not web_service_async_io_task.is_finished():
            job_progress.message = web_service_async_io_task.get_status()
        request_result = web_service_async_io_task.get_result()

        audio = img_from_bytes(request_result)
        return result


###
## Ich kann es so machen wie oben beschrieben und die @syntax auch ffür die Klasse nehmen.
## Das ist klug, da dann die request modifiziert wird und ich so weiß was abgeht.
## Es ist negativ, da ich dadurch das syntax highlighting verliere..
## Oder: es wird ein ServiceClientAPI(service_name) initiert und dann die methoden gewrapped.
## Im Client wird dann auch nur serviceclientapi.request("methodname") gerufen.
## Das sollte den selben effekt haben.
socaity_job_manager = JobManager()


class newFace2Face(ServiceClientAPI):

    def __init__(self, service_url: str = "localhost"):
        super().__init__(service_nanme="", service_url=service_url)

    @socaity_job_manager.job
    def swap_one(self, source_img: np.array, target_img: np.array) -> np.array:
        return self.request("swap_one", source_img, target_img)
