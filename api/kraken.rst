.. automodule:: kraken

   .. autofunction:: kraken.make_absolute_url

   .. autofunction:: kraken.redirect

   .. autofunction:: kraken.runserver

   .. automodule:: kraken.site
      :members: expose_template, Request, StaticFileResponse, TemplateResponse

      .. autoclass:: kraken.site.Site
         :members: __call__, import_, prehandle, register_controllers,
             register_engine, register_endpoint, render_template,
             simple_template

   .. automodule:: kraken.template

      .. autoclass:: kraken.template.BaseEngine
         :members:

      .. autodata:: kraken.template.BUILTIN_ENGINES

      .. automodule:: kraken.template.jinja2_
         :members:

      .. automodule:: kraken.template.mako_
         :members:

      .. automodule:: kraken.template.genshi_
         :members:

      .. automodule:: kraken.template.python
         :members:

      .. automodule:: kraken.template.str_format
         :members:
