# backend/factories/base.py
from abc import ABC, abstractmethod
import random
import string
import datetime
from sqlalchemy import ForeignKeyConstraint
import yaml
import os
from decimal import Decimal
from collections import defaultdict
from typing import Dict, Any, Type, List, Optional
from sqlalchemy.orm import Session, class_mapper
from contextlib import contextmanager



class DependencyResolver:
    def __init__(self, models_module):
        self._dependency_graph = defaultdict(set)
        self._model_registry = {}
        self._models_module = models_module
        self._resolved_orders = {}
        self._build_registry()
        self._analyze_all_dependencies()

    def _build_registry(self):
        for name in dir(self._models_module):
            attr = getattr(self._models_module, name)
            if isinstance(attr, type) and hasattr(attr, '__tablename__'):
                self._model_registry[name] = attr

    def _get_model_by_tablename(self, tablename):
        for model in self._model_registry.values():
            if model.__tablename__ == tablename:
                return model
        return None

    def _analyze_all_dependencies(self):
        for name, model_class in self._model_registry.items():
            mapper = class_mapper(model_class)
            
            # 1. Analisis dari Relationships (Cara Utama)
            for prop in mapper.relationships:
                if prop.direction.name == 'MANYTOONE':
                    related_model_name = prop.mapper.class_.__name__
                    if name != related_model_name:
                        self._dependency_graph[name].add(related_model_name)
            
            # 2. Analisis dari ForeignKeyConstraints (Cara Cadangan)
            for constraint in mapper.mapped_table.constraints:
                if isinstance(constraint, ForeignKeyConstraint):
                    for fk in constraint.elements:
                        target_table = fk.column.table.name
                        related_model = self._get_model_by_tablename(target_table)
                        if related_model:
                            related_model_name = related_model.__name__
                            if name != related_model_name:
                                self._dependency_graph[name].add(related_model_name)

    def get_dependencies(self, model_name: str) -> List[str]:
        if model_name in self._resolved_orders:
            return self._resolved_orders[model_name]

        visiting = set()
        visited = set()
        order = []

        def dfs(name):
            visiting.add(name)
            for dep in sorted(list(self._dependency_graph.get(name, []))):
                if dep in visiting:
                    continue
                if dep not in visited:
                    dfs(dep)
            visiting.remove(name)
            visited.add(name)
            if name != model_name:
                order.append(name)
        
        if model_name not in visited:
            dfs(model_name)

        self._resolved_orders[model_name] = order
        return order
    
class MainTestDataFactory:
    def __init__(self, session: Session, models_module):
        self.session = session
        self.models_module = models_module
        self._builders: Dict[str, callable] = {}
        self._created_objects = defaultdict(list)
        self._unique_counters = defaultdict(int)
        self._dependency_resolver = DependencyResolver(models_module)

        # Inisialisasi module factories
        self.master = MasterDataFactory(self)
        self.purchase = PurchaseFactory(self)
        self.inventory = InventoryFactory(self)
        self.sales = SalesFactory(self)
        self.finance = FinanceFactory(self)
        self.production = ProductionFactory(self)
        # Tambahkan modul lain di sini nanti, misal: self.sales = SalesFactory(self)

    def register_builder(self, model_name: str, builder_func: callable):
        self._builders[model_name] = builder_func

    def get_unique_value(self, prefix: str, total_length: int = 8) -> str:
        self._unique_counters[prefix] += 1
        counter_str = str(self._unique_counters[prefix])
        
        # Hitung sisa panjang yang dibutuhkan untuk random string
        random_len = total_length - len(prefix) - len(counter_str) - 1 # -1 untuk tanda hubung
        if random_len < 1:
            # Jika prefix dan counter sudah terlalu panjang, potong saja
            return (prefix + counter_str)[:total_length]
            
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random_len))
        return f"{prefix}{self._unique_counters[prefix]}-{random_suffix}"

    def get_model_class(self, model_name: str) -> Type:
        return getattr(self.models_module, model_name)
    
    def clear_cache(self):
        self._created_objects.clear()
        self._unique_counters.clear()

    def create(self, model_name: str, **overrides: Any) -> Any:
        reuse_strategy = overrides.pop('_reuse', 'create_new')
        if reuse_strategy == 'reuse_existing' and self._created_objects[model_name]:
            return random.choice(self._created_objects[model_name])

        dependencies = self._dependency_resolver.get_dependencies(model_name)
        
        for dep_name in dependencies:
            if dep_name not in overrides and dep_name.lower() not in overrides:
                # Ciptakan dependensi jika tidak disediakan
                dep_instance = self.create(dep_name, _reuse='reuse_existing')
                overrides[dep_name.lower()] = dep_instance

        if model_name not in self._builders:
            raise ValueError(f"No builder registered for model '{model_name}'")

        instance = self._builders[model_name](overrides)
        
        self.session.add(instance)
        self._created_objects[model_name].append(instance)

        return instance

class BaseModuleFactory(ABC):
    def __init__(self, main_factory: MainTestDataFactory):
        self.main_factory = main_factory
        self.session = main_factory.session
        self._register_builders()

    @abstractmethod
    def _register_builders(self):
        pass

    def create(self, model_name: str, **kwargs: Any) -> Any:
        return self.main_factory.create(model_name, **kwargs)

# Import di sini untuk menghindari circular import
from .master_data import MasterDataFactory
from .purchase import PurchaseFactory
from .inventory import InventoryFactory
from .sales import SalesFactory
from .finance import FinanceFactory
from .production import ProductionFactory

@contextmanager
def test_session_scope(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    
    from backend.app import db_models
    factory = MainTestDataFactory(session, db_models)
    
    try:
        yield session, factory
    finally:
        session.close()
        transaction.rollback()
        connection.close()