---
title: 'Using Aliases in Bash'
data: 2019-06-14
permalink: /posts/2019/06/blog_post_bash_alias/
tags:
  - bash
  - alias
  - command line
---


What are aliases in bash?
-------------------------
If you are tired of typing out the same long command over and over again, it's time to set up a few bash aliases. Aliases allow you to create shortcut commands for longer ones. For example, instead of typing out `ls -l`, you could type `ll` + `Enter` to save time. 


How do you set up an alias?
---------------------------
In order to set up an alias, you will need to be familiar with a text editor (like [vim](/https://fnew.github.io/posts/2019/05/blog_post_getting_started_vim/)!) and the `.bashrc` or `.bash_profile` files. On Unix operating systems, these files will typically be located in the user's home directory. There is a subtle difference between these two files, which is related to the difference between *login* and *non-login* shells (which is not important for now):
  
  * The .bashrc file is reloaded every time you start a new copy of Bash.
  * The .bash_profile file is loaded only when you log in (or use a flag to tell Bash to act as a login shell).
    
It is typical to put aliases into the `.bashrc` file, and to reference your `.bashrc` file in the `.bash_profile`. If you ever make changes to your `.bashrc`, you just need to type `bash` into the command line to reload the file. 

A bash alias has the following structure:
  
`alias [alias_name]="[long_command_to_alias]"`
 
Each alias is on a new line and begins with the command `alias`, followed by your desired shortcut, an `=`, and then the full command that you do not want to type anymore. 

### Example:

Using combinations of options with `ls` on the command line is very useful, but can get clunky. A common command is: `ls -lhaG`. (This tells the shell to list the contects of a directory in long format, showing hidden files, with human-readable sizes, and hide the group names.) Instead of typing `ls -lhaG` everytime, it would be much easier to type `ll`.

`$ vi ~/.bashrc`

This will open your `.bashrc ` file in vim. Now that you are in vim, or whatever text editor you prefer, add the following:

`alias ll="ls -lhaG"`

Save and close the `.bashrc` file now. Since we've added this to the `.bashrc` file, we now need to type `bash` and Enter on the command line, and now the alias will be live. Try typing `ll` to see what happens. 


What are my favorite aliases?
-----------------------------

I use aliases for ssh commands, common bash command combinations, and for moving around common directories.

SSH to a remote server:
`alias server="ssh fnn@made.up.server.edu"` 

Changing directories to my home base from any location:
`alias wrk="cd /my/working/directory"` 

Starting Rstudio Server
`alias rstud="/programs/rstudio_server/rstudio_start"`


More information and examples
-----------------------------
There are many guides available online for setting up and understanding aliases. 

[You can see nixCraft's list of 30 useful aliases for bash here](https://www.cyberciti.biz/tips/bash-aliases-mac-centos-linux-unix.html). 

[DigitalOcean has also published examples of useful aliases](https://www.digitalocean.com/community/tutorials/an-introduction-to-useful-bash-aliases-and-functions). 

And finally, [you can find similar information and a video on aliases here](https://mijingo.com/blog/creating-bash-aliases).

