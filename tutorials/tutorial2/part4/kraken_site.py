import kraken
from kraken.site import Site

import controllers
import blog_kalamar


site = Site(kalamar_site=blog_kalamar.site)
site.register_controllers(controllers)

if __name__ == "__main__":
    kraken.runserver(site)

