---
title: 'Using RStudio Server'
data: 2019-04-26
permalink: /posts/2019/04/blog_post_rstudio_server/
tags:
  - Rstudio
  - server
  - brito lab
---

We now have RStudio Server installed on all CBSU machines! This means that you can run a hosted RStudio session in your browser and not worry about copying over files from the server, or running out of memory on your own machine. Here are the steps you need to follow to use it.

1. Log onto the server using a shell prompt. Use Terminal on MacOS or download and install Putty for Windows.
      
      ssh your.user.id@cbsubrito.tc.cornell.edu   #Log onto whichever machine you typically use

2. Once you have logged onto the server, start the RStudio-Server daemon by typing and running the following command: 

      /programs/rstudio_server/rstudio_start
      
3. Next, open a web browser and paste this into the address bar:

      http://cbsubrito.biohpc.cornell.edu:8015
      
4. You will be prompted to enter you user ID and password. Log in using your biohpc login credentials and you are done.
