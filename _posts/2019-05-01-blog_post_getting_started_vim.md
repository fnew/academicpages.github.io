---
title: 'Getting started with Vim'
data: 2019-05-01
permalink: /posts/2019/05/blog_post_getting_started_vim/
tags:
  - vi
  - vim
  - text editor
  - how to exit vim
---

How to get started using my favorite text editor. 

To begin with, let's talk about how to exit vim, do the following:

Hit the `Esc` key to enter "Normal mode". Then you can type `:` to enter "Command-line mode". A colon (`:`) will appear at the bottom of the screen and you can type in one of the following commands. To execute a command, press the `Enter` key.

* `:q` to quit (short for :quit)
* `:q!` to quit without saving (short for :quit!)
* `:wq` to write and quit

I start with this because [this is the most asked question on stack overflow](https://stackoverflow.blog/2017/05/23/stack-overflow-helping-one-million-developers-exit-vim/):

>In the last year, How to exit the Vim editor has made up about .005% of question traffic: that is, one out of every 20,000 visits to Stack Overflow questions. That means during peak traffic hours on weekdays, there are about 80 people per hour that need help getting out of Vim.



Opening and Moving around Vim
-----------------
All jokes aside, if you want to open vim, first open a terminal (Terminal in MacOS, or download something like Putty for Windows) and type `vi`. Vim ships with all Unix-based systems, so it will already be installed if you are on MacOS or Linux.

Now that you are inside of vim, you are currently in "Normal mode". Anything you type in this mode will not show up on the screen, but can be used for navigating the file. For instance, &larr;, &uarr;, &darr; and &rarr; are `h`, `j`, `k`, and `l` keys, respectively. You can use `$` to skip to the end of the line or `0` to move to the beginning of the line. [To learn more about moving around in Vim, I recommend this page from Vim fandom](https://vim.fandom.com/wiki/Moving_around).


Editing in Vim
---------------
If you hit the `i` key, you will be in "Interactive mode". This means that anything you type will now appear on the screen. In this mode you can still move around the file, but you will need to use the arrow keys. Hit `Esc` to go back to "Normal mode" to move around using keyboard commands again. Don't forget, in order to exit Vim, you will need to hit `Esc` first to exit "Interactive mode", then you can type `:q`, `:wq`, or `:!q`.


Tutorials
---------
Vim is considered to be unintuitive, but I think that with some help getting started, it can become second nature.

[This is an awesome guide/cheat sheet for using vim](https://stac47.github.io/vim/cheat/sheet/2014/02/22/vim-advanced-cheat-sheet.html).

[Open Vim is an interactive tutorial for learning how to use it](https://www.openvim.com).

[Another place to learn vim](https://danielmiessler.com/study/vim/).


Plugins
-------
There are SO many plugins available for vim. [VimAwesome](https://vimawesome.com) is a collection of all vim plugins available for download. You can find many lists like "10 best vim plugins for developers".

My favorite plugin for productivity is called ConqueTerm. ConqueTerm allows you to open an interactive shell inside of vim. This means that while you edit a text file, you have run an interactive python, R, bash, or any type of shell in a split screen window. I use this to interactively test code while I write it in vim.

To get and install ConqueTerm, download the latest (v2.3) [vimball here](https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/conque/conque_2.3.vmb). Then open the .vba file in vim, `vi conque_2.3.vmb` and type `:so % > :q`.


Go try!
-------
Good luck getting started with vim and keep at it, it is definitely worth it!
