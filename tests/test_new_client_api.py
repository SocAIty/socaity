from socaity.socaity_client.definitions.enums import ModelDomainTag
from socaity.socaity_client.jobs.threaded.internal_job import InternalJob
from socaity.socaity_client.service_client_api import ServiceClientAPI
from socaity.socaity_client.web.service_client import ServiceClient

srvc_fries_maker = ServiceClient(
    service_url="localhost:8000/api",
    model_name="friesmaker",
    model_domain_tags=[ModelDomainTag.IMAGE, ModelDomainTag.AUDIO],
    model_tags=None
)
srvc_fries_maker.add_endpoint(endpoint_route="kartoffel", file_params={"image": bytes})
srvc_fries_maker.add_endpoint(
    endpoint_route="make_fries",
    file_params={"potato_one": bytes, "potato_two": bytes, "potato_three": bytes}
)
fries_maker_client_api = ServiceClientAPI(srvc_fries_maker)

class FriesMaker:

    @fries_maker_client_api.job()
    def _kartoffel(self, job: InternalJob, image: bytes):
        """
        Swaps a face from source_img to target_img;
        in the manner that the face from source_img is placed on the face from target_img.
        :param source_img: The image containing the face to be swapped. Read with open() -> f.read()
        :param target_img: The image containing the face to be swapped to. Read with open() -> f.read()
        """
        endpoint_request = job.request_sync(endpoint_route="kartoffel", image=image)

        if endpoint_request.error is not None:
            raise Exception(f"Error in making fries: {endpoint_request.error}")

        return endpoint_request.result

    @fries_maker_client_api.job()
    def _make_fries(self, job: InternalJob, potato_one: bytes, potato_two: bytes, potato_three: bytes):
        endpoint_request = job.request_sync(endpoint_route="make_fries", potato_one=potato_one, potato_two=potato_two, potato_three=potato_three)

        if endpoint_request.error is not None:
            raise Exception(f"Error in making fries: {endpoint_request.error}")

        return endpoint_request.result

    def make_fries(self, potato_one: str, potato_two) -> InternalJob:
        """
        Swaps a face from source_img to target_img;
        in the manner that the face from source_img is placed on the face from target_img.
        :param source_img: Path to the image containing the face to be swapped.
            Or the image itself as bytes (with open(f): f.read()) .
        """
        #with open(potato_one, "rb") as f:
        #    potato_one = f.read()
        with open(potato_two, "rb") as f:
            potato_two = f.read()

        return self._make_fries(open(potato_one, "rb"), potato_two, potato_two)



img_1 = "A:\\projects\\_face2face\\face2face\\test\\test_imgs\\test_face_1.jpg"
img2 = "A:\\projects\\_face2face\\face2face\\test\\test_imgs\\test_face_2.jpg"

fries_maker = FriesMaker()
job = fries_maker.make_fries(img_1, img2)
job.run_sync()
a = 1