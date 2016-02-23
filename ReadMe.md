
These are just some tools to manage reveal.js based slide decks.

## Splitting slide decks

Once the slide deck has been created with tools like slides.com, it may be useful to break it down in small parts :

 - to remove or reorganize slides
 - to allow easy collaboration in git

This is the goal os the `split.py` script

     python split.py -i source.html -o ouputdir

In the selected outputdir a tree of files will be generated :

 - each slide is a separated file
 - each nested slidedeck in reveal is in a sub folder     

## Assembling the slides

The `assemble.py` can be used to assemble a slides that are split is separated files.

A typical tree would be something like :

    src/
    └── slides
        ├── 00-cover.md
        ├── 01-2012
        │   ├── 01.md
        │   ├── 02.md
        │   └── 03.md
        └── 02-2013
            ├── 01.md
            └── 02.md

Each individual slide starts with a header that contains meta-data

    @template:title
    @title:Sample Title 1
    @subtitle:Sample Sub Title
    @notes:This is my speaker note

The template will be taken from the `templates` folder and use simple python templating.


    python assemble.py  -c <slides.config> -i <inputdir> -o <outputfile>

The slides.config file is used to provide common meta-data



