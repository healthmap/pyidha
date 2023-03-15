def create_chunks(array, size):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(array), size):
        yield array[i : i + size]
