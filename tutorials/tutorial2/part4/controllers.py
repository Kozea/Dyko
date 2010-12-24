from kraken.site import expose_template, expose
from kraken import redirect
from datetime import datetime

import blog_kalamar


@expose_template("/post/<int:post_id>")
def blog_post(request, post_id, **kwargs):
    post = blog_kalamar.site.open("blog_entry", {"id": post_id})
    return {"blog_entry": post}

@expose("/post/add", methods=("POST",))
def add_blog_post_process(request, **kwargs):
    title = request.values["title"]
    content = request.values["content"]
    submitted = datetime.now()
    new_post_properties = {
        "title": title,
        "content": content,
        "submitted": submitted}
    new_post = blog_kalamar.site.create("blog_entry", new_post_properties)
    new_post.save()
    return redirect(request, "/", status=303)
