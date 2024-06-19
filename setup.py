from setuptools import setup, find_packages

setup(
    name='socaity',
    version='0.0.2',
    description="Interface for hosted AI models. "
                "Generative AI: text2voice, voice2voice, face2face, etc."
                "Supports locally hosted and remote endpoints.",
    author='SocAIty',
    packages=find_packages(),
    install_requires=[
        'socaity-client',
        'tqdm',
        'soundfile'
    ]
)