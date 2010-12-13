from kalamar_site import site
from kalamar.request import Condition, And, Or

def print_results(condition):
    print "Results for condition: %s" % condition
    for item in site.search('blog_entry', condition):
        print 'Post ID #%s : %s ' % (item['id'], item['title'])
        print item['content']
    print ""

condition = Condition('title', '=', 'Kalamar is Kool')

print_results(condition)

condition = Condition('title', 'like', '%blog post')

print_results(condition)

condition = And(
        Condition('title', 'like', '%blog post'),
        Condition('content', 'like', '%even%'))

print_results(condition)

condition = Or(
        Condition('title', 'like', '%blog post'),
        Condition('title', '=', 'Kalamar is Kool'))

print_results(condition)
