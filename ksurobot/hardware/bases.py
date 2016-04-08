class AbstractPart(object):
    def __enter__(self):
        return self

    def __exit__(self, *enc):
        pass
