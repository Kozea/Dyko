def dump_item(item):
    """Dump item informations."""
    data = (item["artist"], item["album"], item["track"], item["title"],
            item["ext"])
    print "Artist: %s - Album: %s - Track: %s - Title: %s - Extension: %s" % data
