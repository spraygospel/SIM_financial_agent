# backend/factories/system.py
from .base import BaseModuleFactory
from backend.app import db_models

class SystemFactory(BaseModuleFactory):
    def _register_builders(self):
        self.main_factory.register_builder("User", self._build_user)
        self.main_factory.register_builder("Role", self._build_role)
        self.main_factory.register_builder("Menu", self._build_menu)
        self.main_factory.register_builder("MenuList", self._build_menu_list)

    def _build_user(self, params):
        return db_models.User(
            User=params.get('User', self.main_factory.get_unique_value('user', 16)),
            Name='Test User', Password='password', Role='TESTER', Language='EN',
            WhatsAppNo='', Email=''
        )

    def _build_role(self, params):
        user = params.get('user') or self.main_factory.create('User')
        return db_models.Role(
            Role=params.get('Role', 'TESTER'),
            User=user.User
        )

    def _build_menu(self, params):
        return db_models.Menu(
            Role=params.get('Role', 'TESTER'),
            Menu=params.get('Menu', 'TestMenu'),
            SubMenu=params.get('SubMenu', 'TestSubMenu')
        )

    def _build_menu_list(self, params):
        menu = params.get('menu') or self.main_factory.create('Menu')
        return db_models.MenuList(
            Menu=menu.Menu,
            SubMenu=menu.SubMenu,
            Filename='test.dll',
            FormName='frmTest'
        )