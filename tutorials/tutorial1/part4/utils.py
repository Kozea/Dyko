from datetime import timedelta

def dump_item(item):
        data = (item['artist'], item['album'], item['track'],
                item['title'], timedelta(milliseconds=item['duration']))
        print "Artist: %s Album: %s Track : %s Title: %s Duration : %s " % data
        print "Copyright : %s" % item['copyright']
