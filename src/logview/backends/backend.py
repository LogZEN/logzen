from abc import ABCMeta, abstractmethod

class Result:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_count(self):
        pass

    @abstractmethod
    def get_rows(self,
                 offset,
                 count):
        pass

class Backend:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_logs(self):
        pass
