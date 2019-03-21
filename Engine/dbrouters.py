# -*- coding: utf-8 -*-

from Composition.models import Ingredient
from Product.models import Product


class MyDBRouter(object):
    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        if model in [Ingredient, Product]:
            return "data"
        if model == Product:
            return "data"
        return "default"

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        if model == Ingredient:
            return "data"
        if model == Product:
            return "data"
        return "default"
