# module webpage.content in webpage

## Name

webpage.content - # -*- coding: utf-8 -*-

## Classes Tree

```text
+-- __builtin__.object
|  +-- PageContent
```

## Classes

### class **PageContent**(__builtin__.object)
Page Content

#### extract(self, xpath=None)
*extract content by xpath*


#### links(self)
*extract links*


#### make_links_absolute(self)
*makes all links in the document absolute, assuming that 
base_href is the URL of the document.*


#### make_links_offline(self, offline_links={})
*Rename links in the document for offline use.

if offline_links is not defined, rename all links*


#### remove(self, xpath=None)
*remove content by xpath*


#### save(self, filename)
*save content to file*


#### to_unicode(self)
*convert content to unicode*


