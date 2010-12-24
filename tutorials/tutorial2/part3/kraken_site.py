import kraken
from kraken.site import Site

import blog_kalamar


site = Site(kalamar_site=blog_kalamar.site)

if __name__ == "__main__":
    kraken.runserver(site)
