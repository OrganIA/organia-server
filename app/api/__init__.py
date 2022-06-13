from pathlib import Path
import importlib

from app.utils.bp import Blueprint


bp = Blueprint(__name__)


@bp.get('/')
def root():
    from .info import get_info
    return get_info()


"""
Will auto-register blueprints from every Python file in the adjacent directory,
as long as they are at module-level and called "bp"
"""
for file in Path(__file__).parent.glob('*'):
    if file.stem.startswith('_'):
        continue
    print(file)
    module = importlib.import_module(f'{__name__}.{file.stem}')
    if not hasattr(module, 'bp'):
        continue
    print('Registering', module)
    bp.register_blueprint(module.bp)
