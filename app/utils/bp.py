from flask import Blueprint as Base


class Blueprint(Base):
    def __init__(self, module_name: str, prefix=True):
        name = module_name.replace('.', '_')
        print(module_name, name)
        if isinstance(prefix, str):
            prefix = prefix
        elif prefix:
            prefix = '/' + module_name.split('.')[-1]
        else:
            prefix = None
        super().__init__(name, module_name, url_prefix=prefix)
