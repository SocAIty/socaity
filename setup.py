from setuptools import setup, find_packages

setup(
    name='socaity',
    version='0.0.0',
    description="Interface for hosted AI models. "
                "Generative AI: text2voice, voice2voice, face2face, etc."
                "Supports local host and remote endpoints.",
    author='SocAIty',
    packages=find_packages(),
    install_requires=[
        'req',
        'tqdm',
        'req',
        'librosa',
        'soundfile'
    ]
)