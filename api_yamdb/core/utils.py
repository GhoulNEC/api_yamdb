import enum
from datetime import datetime

a = datetime.strptime("2019-09-24T21:08:21.567Z", "%Y-%m-%dT%H:%M:%S.%fZ")


class ChekFieldModel(enum.Enum):
    AutoField = 'int'
    ForeignKey = 'select_related'
    ManyToManyField = 'int'
    IntegerField = 'int'
    DateTimeField = 'datetime'
    TextField = 'str'
    CharField = 'str'
    SlugField = 'str'
