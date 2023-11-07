def join_path(*paths: str) -> str:
    """Join paths with '/', all path will start with '/'."""

    path = "/".join(path.strip("/") for path in paths if path)
    if path.startswith("/"):
        return path
    return "/" + path
