from dataclasses import dataclass
import os

@dataclass
class EnvironmentVariable:
    exchange_rate_url:str=os.getenv("EXCHANGE_RATE_URL")

env_var=EnvironmentVariable()
