import csv
import inspect
import os
from datetime import datetime

from core.exeptions import Fill_DBException
from core.utils import ChekFieldModel
from reviews import models
from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR


class Command(BaseCommand):
    help = u'''Заполнить БД по следующем критериям:
    1) Первым делом заполнить модель User;
    2) Заполнить модели Category / Genre;
    3) Заполнить модель Title;
    4) Заполнить модель GenreTitle;
    5) Последующие модели.
    Если не учесть данную последовательность, то возникнет ошибка,
    т.к. все модели с полями ForeignKey / ManyToManyField ожидают
    экземпляр класса связующей ею моделью. 
    
    Просьба - учесть данный факт!
    '''

    def add_arguments(self, parser):
        parser.add_argument('-m',
                            '--model',
                            type=str,
                            help=u'Модель'
                            )
        parser.add_argument('-f',
                            '--file',
                            type=str,
                            help=u'Имя файла csv'
                            )

    @classmethod
    def get_csv_file(cls, filename):
        name_file = filename + '.csv'
        path = os.path.join(BASE_DIR, 'static', 'data', name_file)
        return path

    @classmethod
    def get_obj_models(cls, model):
        """Почему отправляется не та строка...."""
        classes = [obj for obj in inspect.getmembers(models, inspect.isclass)]
        try:
            for name, obj in classes:
                if name == model.title():
                    return obj
        except AttributeError:
            raise Fill_DBException(
                f'Модель {model} отсутствует в модуле {models}'
            )

    @classmethod
    def chek_field_model(cls, obj, item_dict):
        obj_data = {}
        try:
            for item in item_dict:
                field_name = obj._meta.get_field(item).get_internal_type()
                type_field = ChekFieldModel.__members__.get(field_name)
                if type_field is None:
                    raise Fill_DBException(
                        'Проверьте атрибуты класса ChekFieldModel'
                    )
                if type_field.value == 'int':
                    obj_data[item] = int(item_dict[item])
                elif type_field.value == 'select_related':
                    if item.endswith("_id"):
                        obj_data[item] = int(item_dict[item])
                    else:
                        related_model = obj._meta.get_field(
                            item).related_model
                        obj_data[item] = related_model.objects.get(
                            pk=int(item_dict[item])
                        )
                elif type_field.value == 'datetime':
                    obj_data[item] = datetime.strptime(
                        item_dict[item],
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                else:
                    obj_data[item] = str(item_dict[item])
        except Exception:
            raise
        return obj_data

    def handle(self, *args, **kwargs):
        model = kwargs['model']
        filename = kwargs['file']
        file_path = self.get_csv_file(filename)
        try:
            obj = self.get_obj_models(model)
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=",")
                for dict_data in csv_reader:
                    obj.objects.get_or_create(
                        **self.chek_field_model(obj, dict_data)
                    )
        except FileNotFoundError:
            print(f'Файла с путем {file_path} не существует!')
        except Fill_DBException as err:
            print(err)
        except Exception as err:
            print(f'Возникла ошибка: {err}')
