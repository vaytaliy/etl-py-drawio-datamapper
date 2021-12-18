class Id:
    __id = 0

    @staticmethod
    def get_id():
        Id.__id += 1
        return Id.__id
    
    @staticmethod
    def set_new_increment_position(amount):
        if amount >= Id.__id:
            Id.__id = amount