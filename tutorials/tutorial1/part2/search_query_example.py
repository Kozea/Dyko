#import the previously defined module
from kalamar_site import kalamar_site
from kalamar.request import Condition, And, Or
from utils import dump_item


def search_track_two():
    """Simple function dumping the second track of every album
    """
    print "Searching for track number two accross all albums:"
    for item in kalamar_site.search('music', {'track': 2}):
        dump_item(item)
        print ''

def search_track_between_8_and_10():
    """Simple function illustrating And request"""
    print "Searching for track numbers between 8 and 10 of the 'Hope' album"""
    condition = And(
                    Condition('track', '<=', 10),
                    Condition('track', '>=', 8),
                    Condition('album', '=', 'Hope'))
    for item in kalamar_site.search('music', condition):
        dump_item(item)
        print ''


def search_track_1_or_3():
    """Simple function illustrating Or request"""
    print "Searching for track numbers 1 or 3, for albums which title begins with 'Chapter'"""
    condition = And(
                    Or(
                        Condition('track', '=', 1),
                        Condition('track', '=', 3)),
                    Condition('album', 'like', 'Chapter%'))
    for item in kalamar_site.search('music', condition):
        dump_item(item)
        print ''

if __name__ == '__main__':
    search_track_two()
    print ''
    search_track_between_8_and_10()
    print ''
    search_track_1_or_3()
    print ''

