# module webpage.cleaner in webpage

## Name

webpage.cleaner

## Classes Tree

```text
+-- lxml.html.clean.Cleaner(__builtin__.object)
|  +-- CleanerProfile
```

## Classes

### class **CleanerProfile**(lxml.html.clean.Cleaner)
Webpage cleaner profile

remove the all or partially suspicious content from this
unparsed document. It supports removing embedded or script
content, special tags, CSS style annotations and much more.

#### allow_element(self, el)
**


#### allow_embedded_url(self, el, url)
**


#### allow_follow(self, anchor)
*Override to suppress rel="nofollow" on some anchors.*


#### clean_html(self, html)
**


#### kill_conditional_comments(self, doc)
*IE conditional comments basically embed HTML that the parser
doesn't normally see.  We can't allow anything like that, so
we'll kill any comments that could be conditional.*


