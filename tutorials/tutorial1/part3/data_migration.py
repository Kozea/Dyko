from kalamar_site import kalamar_site

def migrate_file_system():
    items = 0

    print "Migrating items: ",
    for item in kalamar_site.search("old_music"):
        print ".",
        items += 1
        properties = {
            "artist": item["artist"],
            "album": item["album"],
            "duration": item["duration"],
            "copyright": item["copyright"],
            "track" : item["track"],
            "title": item["title"]}
        db_item = kalamar_site.create("music", properties)
        db_item.save()
    print
    print "%i items migrated" % items

if __name__ == "__main__":
    migrate_file_system()
