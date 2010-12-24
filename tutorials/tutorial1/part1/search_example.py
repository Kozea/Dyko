# Import the previously defined module
from kalamar_site import kalamar_site
from utils import dump_item

def dump_db():
    """Dump the first five items from the access point."""
    for item in list(kalamar_site.search("music"))[:5]:
        dump_item(item)
        print

if __name__ == "__main__":
    dump_db()
