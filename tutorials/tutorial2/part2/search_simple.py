from kalamar_site import site


for item in site.search("blog_entry"):
    print "Post ID #%s: %s" % (item["id"], item["title"])
    print item["content"]
