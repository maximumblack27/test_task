import enum


class BaseEnum(enum.Enum):

    @classmethod
    def get_values(cls):
        return [item.value for item in cls]


class BookColumnEnum(BaseEnum):
    ID = 'id'
    NAME = 'name'
    AUTHOR = 'author'
    DATE_PUBLISHED = 'date_published'
    GENRE = 'genre'
