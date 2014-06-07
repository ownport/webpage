# module webpage.page in webpage

## Name

webpage.page

## Description

# -*- coding: utf-8 -*-
#
#   Simple web archive format
#

## Classes Tree

```text
+-- __builtin__.object
|  +-- Webpage
```

## Classes

### class **Webpage**(__builtin__.object)
Simple Web page archiver

#### clean(self, cleaner_profile)
*clean content by cleaner profile*


#### get_resources(self, pattern=None)
*fetch resources (images, css, javascript, video, ...)*


#### remove(self, xpath=None)
*remove content by xpath*


#### save(self, filename='index', metadata=True, resources=True)
*save metadata and content

filename - defines just filename for three files: 
    - <filename>.html 
    - <filename>.metadata 
    - <filename>.resources

Only the first one is HTML file, the rest of files are JSON files

metadata - if True, HTTP response information will be stored into .metadata file
resources - If True, resources metadata will be stores into .resources file*


