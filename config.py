from dataclasses import dataclass

@dataclass
class DbConfig:
    uri: str = "mongodb+srv://prodata:8aBewnk0T7UFVarG@prodata.tkoenit.mongodb.net/?retryWrites=true&w=majority&appName=ProData"  # Replace with your cluster link
    name: str = "nofap_tracker"  # Database name

@dataclass
class Misc:
    admin_ids: list[int] = (123456789,)  # Replace with actual admin IDs
    bot_token: str = "7558223351:AAFnhlfL2OurarbjJAkoXHFd6E4F3kQIxzQ"  # Replace with actual token
    webapp_url: str = "https://mtbilla213.github.io/"  # Replace with actual webapp URL

@dataclass
class Strings:
    # Bot messages
    start_message: str = "Welcome to NoFap Tracker!\nClick the button below to start tracking:"
    webapp_button: str = "📊 Open Tracker"

    # Error messages 
    error_db: str = "Database error occurred. Please try again later."
    error_unknown: str = "Unknown error occurred. Please try again."

@dataclass
class Config:
    misc = Misc()
    db = DbConfig()
    strings = Strings()