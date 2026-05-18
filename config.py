import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")
REPO_DIR = os.path.join(TEMP_DIR, "repo")

SERVER_URL = "http://localhost:8080"
DEFAULT_ENDPOINT = "/ping"

JAVA_PATHS = {
    8: r"C:\Java\jdk8",
    11: r"C:\Java\jdk11",
    17: r"C:\Java\jdk17",
    21: r"C:\Java\jdk21"
}