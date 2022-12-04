from flask import Blueprint as Base

from app import auth as auth_module


class Blueprint(Base):
    def __init__(self, module_name: str, prefix=True, auth=True, **perms):
        name = module_name.replace('.', '_')
        if isinstance(prefix, str):
            prefix = prefix
        elif prefix:
            prefix = '/' + module_name.split('.')[-1]
        else:
            prefix = None
        super().__init__(name, module_name, url_prefix=prefix)

        if auth:
            self.before_request(lambda: auth_module.check(**perms))
