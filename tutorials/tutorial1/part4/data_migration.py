from kalamar_site import kalamar_site

def migrate_file_system():
    print "Migrating items: ",
    items = 0
    for item in kalamar_site.search('file'):
        print ".",
        items += 1
        db_item = kalamar_site.create('music',{
            'artist': item['artist'],
            'album': item['album'],
            'duration': item['duration'],
            'copyright': item['copyright'],
            'track' : item['track'],
            'title': item['title'],
            'file': item
            })
        db_item.save()
    print
    print "%i items migrated" % items

if __name__ == '__main__':
    migrate_file_system()


