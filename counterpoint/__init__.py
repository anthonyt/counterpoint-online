from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from counterpoint.models import appmaker

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    get_root = appmaker(engine)
    config = Configurator(settings=settings, root_factory=get_root)
    config.add_static_view('static', 'counterpoint:static', cache_max_age=3600)
    config.add_view('counterpoint.views.view_root',
                    context='counterpoint.models.MyRoot',
                    renderer="templates/root.pt")
    config.add_view('counterpoint.views.view_model',
                    context='counterpoint.models.MyModel',
                    renderer="templates/model.pt")
    return config.make_wsgi_app()
