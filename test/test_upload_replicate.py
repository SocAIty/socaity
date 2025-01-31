from asyncio import get_event_loop

import httpx
from media_toolkit import VideoFile, MediaFile




async def async_upload_replicate(file):
    #headers = {"Authorization": "Bearer " + "mytoken.."}
    try:
        file = MediaFile().from_any(file)
        client = httpx.AsyncClient()
        files = {"content": file.to_httpx_send_able_tuple()}

        uploaded_file = await client.post(
            url="https://api.replicate.com/v1/files",
            files=files, headers=headers, timeout=60
        )
    except Exception as e:
        print(f"An error occurred during async upload: {e}")
        return False

    try:
        data = uploaded_file.json()
    except:
        data = {}

    file_url = data.get("urls", {}).get("get", None)
    return file_url


async def __main__():
    vf = VideoFile().from_file("test_files/face2face/test_video_ultra_short.mp4")
    await async_upload_replicate(vf)

if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(__main__())


#except:
#
#async def upload_file(vf):
#client = httpx.AsyncClient()
#headers = {"Authorization": "Bearer " + "r8_5pQCA2nQKutUuWi29PFABi6tq3eQuNG0IJpyV" }
#files = {"content": vf.to_httpx_send_able_tuple()}
#
#uploaded_file = await client.post(url="https://api.replicate.com/v1/files",
#            files=files, headers=headers, timeout=60)
#
#
#try:
#    data = uploaded_file.json()
#except:
#    data = {}
#
#file_url = data.get("urls", {}).get("get", None)
#if file_url:
#    file = httpx.get(file_url, headers=headers, timeout=60)
#
#
#a = 1
#
#
#def _create_file_params(
#    file: Union[BinaryIO, io.IOBase],
#    **params: Unpack["Files.CreateFileParams"],
#) -> Dict[str, Any]:
#    file.seek(0)
#
#    if params is None:
#        params = {}
#
#    filename = params.get("filename", os.path.basename(getattr(file, "name", "file")))
#    content_type = (
#        params.get("content_type")
#        or mimetypes.guess_type(filename)[0]
#        or "application/octet-stream"
#    )
#    metadata = params.get("metadata")
#
#    data = {}
#    if metadata:
#        data["metadata"] = json.dumps(metadata)
#
#    return {
#        "files": {"content": (filename, file, content_type)},
#        "data": data,
#    }