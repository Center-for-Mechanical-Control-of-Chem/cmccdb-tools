
import abc
import collections
from molscribe import MolScribe
from huggingface_hub import hf_hub_download
from PIL import Image
import torch
import tempfile

__all__ = [
    "ImageSMILESGenerator",
    "MolScribeSMILESGenerator"
]

class ImageSMILESGenerator(metaclass=abc.ABCMeta):

    IdentifiedCompound = collections.namedtuple("IdentifiedCompound", ["smiles", "image", "confidence"])
    @abc.abstractmethod
    def identify_smiles(self, image:Image) -> IdentifiedCompound:
        ...

class MolScribeSMILESGenerator(ImageSMILESGenerator):

    def __init__(self):
        self.model = self.load_model()

    @classmethod
    def load_model(cls):
        ckpt_path = hf_hub_download('yujieq/MolScribe', 'swin_base_char_aux_1m.pth')
        return MolScribe(ckpt_path, device=torch.device('cpu'))

    IdentifiedCompound = collections.namedtuple("IdentifiedCompound", ["smiles", "image", "confidence"])
    def identify_smiles(self, image: Image) -> IdentifiedCompound:
        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.png') as file:
            image.save(file, format='png')
            file.flush()
            file.seek(0)
            output = self.model.predict_image_file(file.name, return_atoms_bonds=True, return_confidence=True)
        return self.IdentifiedCompound(output['smiles'], image, output.get('confidence'))
