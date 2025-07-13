def read_file(path: str) -> str:
    """
    Read the contents of a text file.

    Args:
        path (str): The file path to read from

    Returns:
        str: The contents of the file as a string

    Raises:
        FileNotFoundError: If the specified file does not exist
        IOError: If there's an error reading the file
    """
    with open(path, mode="r", encoding="utf-8") as file:
        return file.read()


def write_file(path: str, content: str) -> None:
    """
    Write content to a text file.

    Args:
        path (str): The file path to write to
        content (str): The content to write to the file

    Raises:
        IOError: If there's an error writing to the file
    """
    with open(path, mode="w", encoding="utf-8") as file:
        file.write(content)