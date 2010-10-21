.. automodule:: kraken

   .. autofunction:: kraken.make_absolute_url

   .. autofunction:: kraken.redirect

   .. autofunction:: kraken.runserver

   .. automodule:: kraken.site
      :members: Request, StaticFileResponse, TemplateResponse

      .. autoclass:: kraken.site.Site
         :members: __call__, import_, register_engine, render_template

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
