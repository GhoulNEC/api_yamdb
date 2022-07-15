import csv
import inspect
import os
from datetime import datetime

from django.db import IntegrityError

from core.exeptions import Fill_DBException
from core.utils import ChekFieldModel
from reviews import models
from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR


class Command(BaseCommand):
    help = u'Заполнить таблицы БД'

    def add_arguments(self, parser):
        parser.add_argument('-m',
                            '--model',
                            type=str,
                            help=u'Модель'
                            )
        parser.add_argument('-f',
                            '--file',
                            type=str,
                            help=u'Путь файла с данными csv'
                            )

    def get_csv_file(self, filename):
        name_file = filename + '.csv'
        path = os.path.join(BASE_DIR, 'static', 'data', name_file)
        if not os.path.exists(path):
            self.stderr.write(self.style.WARNING('Файл не найден!'))
        return path

    def get_obj_models(self, model):
        """Добавить проверку на наличие классов в модуле."""
        classes = [obj for obj in inspect.getmembers(models, inspect.isclass)]
        for name, obj in classes:
            if name == model.title():
                return obj
        self.stderr.write(self.style.WARNING('Такой модели нет!'))

    def chek_field_model(self, obj, item_dict):
        obj_data = {}
        for item in item_dict:
            field_name = obj._meta.get_field(item).get_internal_type()
            type_field = ChekFieldModel.__members__[field_name]
            if type_field.value == 'int':
                obj_data[item] = int(item_dict[item])
            elif type_field.value == 'select_related':
                if item.endswith("_id"):
                    obj_data[item] = int(item_dict[item])
                else:
                    related_model = obj._meta.get_field(item).related_model
                    obj_data[item] = related_model.objects.get(
                        pk=int(item_dict[item])
                    )
            elif type_field.value == 'datetime':
                obj_data[item] = datetime.strptime(
                    item_dict[item],
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            else:
                obj_data[item] = item_dict[item]
        return obj_data

    def handle(self, *args, **kwargs):
        model = kwargs['model']
        filename = kwargs['file']
        file_path = self.get_csv_file(filename)
        obj = self.get_obj_models(model)
        try:
            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=",")
                for dict_data in csv_reader:
                    obj.objects.get_or_create(
                        **self.chek_field_model(obj, dict_data)
                    )
        except Fill_DBException as err:
            pass
