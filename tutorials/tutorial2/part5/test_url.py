import sys
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse

from kraken_site import site


if __name__ == "__main__":
    client = Client(site, BaseResponse)
    url = sys.argv[1]
    result = client.get(url)
    print result.data
