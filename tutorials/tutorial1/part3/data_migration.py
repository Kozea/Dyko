from kalamar_site import kalamar_site
from utils import dump_item

def migrate_file_system():
    for item in kalamar_site.search('old_music'):
        db_item = kalamar_site.create('music',{
            'artist': item['artist'],
            'album': item['album'],
            'duration': item['duration'],
            'copyright': item['copyright'],
            'track' : item['track'],
            'title': item['title']})
        db_item.save()

if __name__ == '__main__':
    migrate_file_system()
    for item in kalamar_site.search('music'):
        print item['id']
        dump_item(item)


