from .constants import LOGGER_FILE_PATH


def write_log(msg: str) -> None:
    try:
        with open(file=LOGGER_FILE_PATH, mode="a") as f:
            f.write(f"{msg}\n")
    except Exception:
        print("Please, fill the variable LOGGER_FILE_PATH on ../utils/constants.py")
