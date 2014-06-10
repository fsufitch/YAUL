def iter_chunks(collection, chunksize):
    """
    iter_chunks(collection, chunksize) -> iterator
    
    Get an iterator that returns lists containing chunksize items,
    sequentially extracted from the given collection.
    """
    iterator = iter(collection)
    
    class OutOfInputException(Exception):
        pass
    
    def get_chunk():
        buffer = []
        while len(buffer)<chunksize:
            try:
                buffer.append(iterator.__next__())
            except StopIteration:
                if not buffer: # Couldn't even read one value
                    raise OutOfInputException()
                break
        return buffer
    
    while True:
        try:
            yield get_chunk()
        except OutOfInputException:
            break

    