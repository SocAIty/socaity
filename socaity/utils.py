

def get_sdk_instance(service_name_or_id: str, api_key: str = None):
    """
    Get an instance of the SDK for a given service.
    """
    from fastsdk.fastSDK import FastSDK
    return FastSDK(service_name_or_id, api_key)

