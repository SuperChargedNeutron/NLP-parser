import os

import openai
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.environ["OPENAI_ORGANIZATION"]
openai.api_key = os.environ["OPENAI_KEY"]

BASE_URL = "https://api.openai.com/v1/engines"
SEARCH_URL = "https://api.openai.com/v1/engines/davinci/search"
COMPLETION_URL = "https://api.openai.com/v1/engines/davinci/completions"
