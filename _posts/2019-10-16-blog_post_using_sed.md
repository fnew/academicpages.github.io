---
title: 'Using 'sed''
data: 2019-10-16
permalink: /posts/2019/10/blog_post_using_sed/
tags:
  - bash
  - sed
  - command line
---


Get to know sed: The basics
---------------------------
I want to introduce sed in a quick and informal way for anyone who just wants to get a taste of what sed can do. 

Sed is a (non-interactive) **s**tream **ed**itor. Basically, it takes text as input and then line-by-line does something to that text. It is powerful because it takes direction on specifically *which* lines to perform an operation on. Three of the most common uses of sed are printing, replacement, and deletion, however there are many others. If you only know one use for sed, I think it should be how to find and replace patterns within text.


Find and Replace
-----------------
There may be a time when you need to replace every occurence of a string in a file. Doing this with sed is simple. The basic structure looks like this:

`sed "s/pattern1/pattern2/g" file.txt > newfile.txt`

Where 'pattern1' is what you want to find, and 'pattern2' is what you want to replace it with. By adding the "g" at the end, sed knows to make this replacement at every occurence of 'pattern1', without it, only the first occurence would be replaced.

How would this look in practice?

```console
$ ls
textfile.txt
$ cat textfile.txt
hello world
nice to meet you
$ sed 's/hello/hi/g' textfile.txt > newfile.txt
$ cat newfile.txt
hi world
nice to meet you
```

It is that simple! There are ways to get more advanced with this, including doing in-place editing rather than creating a new file. You do this by adding the '-i' flag and include an extension.

```console
$ sed -i .backup 's/hello/hi/g' textfile.txt
$ ls
textfile.txt
textfile.txt.backup
$ cat textfile.txt
hi world
nice to meet you
$ cat textfile.txt.backup
hello world
nice to meet you
```

To learn more about sed and all of its operations, there are *many* resources available online, some of which I will link here:

[Gymoire sed tutorial by Bruce Barnett](http://www.grymoire.com/unix/sed.html) 

[Complete Sed Command Guide by the Linux Handbook](https://linuxhandbook.com/sed-reference-guide/)

[Useful sed one-liners](http://sed.sourceforge.net/sed1line.txt) (One of many, I'm sure!) 
