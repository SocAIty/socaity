# settings first to set environment variables
from socaity.settings import API_KEYS
from socaity.api import Face2Face, SpeechCraft

from fastsdk import gather_generator, gather_results
from fastsdk.registry import Registry
