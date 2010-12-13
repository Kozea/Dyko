import kraken
import blog_kalamar
import controllers

from kraken.site import Site

site = Site(kalamar_site=blog_kalamar.site)
site.register_controllers(controllers)

if __name__ == '__main__':
    kraken.runserver(site)

