=========
Chapter 2
=========

.. contents::

Data Structure
==============

An example of data structure::

  /
  home/
    music/
      artist/
        album/
          track01 - name1.mp3
          track02 - name2.ogg
          ...

The configuration file of Kzik:
- "url", we define place where music is stored
- "filename_format", indicate the logic format of the music content
- "storage_aliases", give aliases

kzik.conf::

  [track]
  url: file:///home/music
  filename_format: */*/* - *.*
  storage_aliases: artist=path1/album=path2/track=path3/name=path4/format=path5
