from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from counterpoint.models import appmaker

def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    get_root = appmaker(engine)
    config = Configurator(settings=settings, root_factory=get_root)
    # allow jinja2 templates! requires pyramid_jinja2 package.
    config.include('pyramid_jinja2')
    jinja2_extensions=[
        # Allow arbitrary expressions:
        'jinja2.ext.do',
        # Add a trans block tag:
        'jinja2.ext.i18n',
        # Adds break, continue to for loops:
        'jinja2.ext.loopcontrols',
        # Add a with statement for explicit variable scopes:
        'jinja2.ext.with_',
        # Allow autoescaping to be disabled:
        'jinja2.ext.autoescape',
    ]
    for ext in jinja2_extensions:
        config.add_jinja2_extension(ext)
    config.add_jinja2_search_path("counterpoint:templates")
    # add static files folder
    config.add_static_view('static', 'counterpoint:static', cache_max_age=3600)
    # add views
    config.add_view('counterpoint.views.view_exercise',
                    context='counterpoint.models.MyRoot',
                    renderer="exercise.jinja2")
    return config.make_wsgi_app()
