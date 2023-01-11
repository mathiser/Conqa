from abc import abstractmethod


class DBInterface:
    @abstractmethod
    def get_synonym_dictionary(self):
        pass

    @abstractmethod
    def get_volume_number_constraint(self):
        pass

    @abstractmethod
    def get_label_names(self):
        pass