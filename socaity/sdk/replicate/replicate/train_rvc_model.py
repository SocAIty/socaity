from fastsdk.fastSDK import FastSDK
from typing import Union

from media_toolkit import MediaFile


class train_rvc_model(FastSDK):
    """
    Generated client for replicate/train-rvc-model
    """
    def __init__(self, api_key: str = None):
        super().__init__(service_name_or_id="9f4a5c71-0e90-4672-838e-ff3d86dcc273", api_key=api_key)
    
    def predict(self, dataset_zip: Union[MediaFile, str, bytes], epoch: int = 10, version: str = 'v2', f0method: str = 'rmvpe_gpu', batch_size: str = '7', sample_rate: str = '48k', **kwargs):
        """
        Run a single prediction on the model
        
        
        Args:
            dataset_zip: Upload dataset zip, zip should contain `dataset/<rvc_name>/split_<i>.wav`
            
            epoch: Epoch Defaults to 10.
            
            version: Version Defaults to 'v2'.
            
            f0method: F0 method, `rmvpe_gpu` recommended. Defaults to 'rmvpe_gpu'.
            
            batch_size: Batch size Defaults to '7'.
            
            sample_rate: Sample rate Defaults to '48k'.
            
        """
        return self.submit_job("/predictions", dataset_zip=dataset_zip, epoch=epoch, version=version, f0method=f0method, batch_size=batch_size, sample_rate=sample_rate, **kwargs)
     