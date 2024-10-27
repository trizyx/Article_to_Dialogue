from dataclasses import dataclass
import os

from dotenv import load_dotenv
import pandas as pd

from .base import getenv


@dataclass
class Config:
    api_gpt: str
    api_synth:str


def load_config() -> Config:
    load_dotenv()

    return Config(
        api_gpt=os.getenv('API_KEY_GPT'),
        api_synth=os.getenv('API_TINKOFF_GEN_SPEECH'),
    )


config: Config = load_config()
