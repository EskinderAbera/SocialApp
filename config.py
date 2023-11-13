# import os
#
# from pathlib import Path
#
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)
#
#
# class Settings:
#     PROJECT_NAME: str = "SocialApp"
#     PROJECT_VERSION: str = "1.0.0"
#
#     POSTGRES_USER: str = os.getenv("pgadmin")
#     POSTGRES_PASSWORD = os.getenv("1719")
#     POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
#     POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)  # default postgres port is 5432
#     POSTGRES_DB: str = os.getenv("POSTGRES_DB", "socialAPp")
#     DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
#
#
# settings = Settings()
