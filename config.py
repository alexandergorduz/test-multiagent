from pydantic import SecretStr
from pydantic_settings import BaseSettings




class Settings(BaseSettings):

    openai_api_key: SecretStr
    model_name: str

    model_config = {"env_file": ".env"}



settings = Settings()



GRAPH_IMAGE_PATH = "graph.png"

CHECKPOINTER_DB_PATH = "checkpointer.db"

RECURSION_LIMIT = 23

SUMMARIZATION_THRESHOLD = 23
MAX_KEEP_LAST_MESSAGES = 5

MAX_WEB_SEARCH_RESULTS = 3
MAX_WEB_SEARCH_PAGE_SYMBOLS = 1000