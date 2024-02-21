from setuptools import setup, find_packages

setup(
    name='py_audio2face',
    version='0.1.0',
    description="Interface for hosted AI models. "
                "Generative AI: text2voice, voice2voice, face2face, etc."
                "Supports local host and remote endpoints.",
    author='',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm',
        'requests',
        'librosa',
        'soundfile'
    ]
)