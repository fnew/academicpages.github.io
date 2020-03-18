---
title: 'Data Science Tutorials'
date: 2020-03-18
permalink: /posts/2020/03/blog_post_data_science_tutorials/
tags:
  - R
  - data science
  - tutorial
  - learning
---

*A collection of data science, programming, and data visualization tutorials I have found on the internet. Sources referenced.*


A collection of resources and links
=================================
While everyone is transitioning to working from home in order to practice social distancing during the SARS-CoV2 outbreak, lots of scientists are trying to find ways to stay engaged despite not being able to perform experiments. A good use of this time (if you have the mental bandwidth!), is to learn or brush up on coding and data science fundamentals. I've found a number of online tutorials and resources that I want to collect in one place to share with others. These are thrown together so the order may not make sense everywhere.

The Command Line
----------------
The most important thing I learned in my computational biology experience is how to effectively use the command line interface, or CLI, and a shell interpreter, such as Bash. Not every problem requires programming. Some problems are best, and most efficiently, solved using software tools run from the command line or Bash scripting. Here are a few resources that I would recommend for learning about the command line and using bash:
  * Youtube video by Joe Collins ["Begginer's Guide to the Bash Terminal"](https://www.youtube.com/watch?v=oxuRxtrO2Ag)
  * [8 Useful Shell Commands for Data Science](https://www.datacamp.com/community/tutorials/shell-commands-data-scientist)
  * [Bioinformatics 101 by Hadrien Gourle](https://www.hadriengourle.com/tutorials/) tutorials for the command line, file formats, and programs used in NGS data analysis
  * [Linux command line exercises for NGS data](http://userweb.eng.gla.ac.uk/umer.ijaz/bioinformatics/linux.html) by Umer Zeeshan Ijaz
  
I would also recommend learning a text editor that can be used through a terminal. My personal favorite is Vim, [I even wrote a short blog post](https://fnew.github.io/posts/2019/05/blog_post_getting_started_vim/) about it last year. Other CLI text editors include nano and Emacs. All three come installed on all Unix-based operating systems like Linux or MacOS (in other words, any operating system that comes with a terminal).

Learning R
-------------
R is a great language to learn for statistical analyses and data visualization. A good first step in learning to use R is to [download RStudio for desktop](https://rstudio.com/products/rstudio/). RStudio is an integrated development environment, or IDE, for the language R. IDEs are useful for writing, reading, and debugging code. For an introduction to R, [this tutorial from swirl](https://swirlstats.com) lets you learn interactively at your own pace. Here is a text-based [tutorial for learning R from datamentor](https://www.datamentor.io/r-programming/#tutorial).

Within RStudio, you can create documents of your work using RMarkdown. These are useful for reproducibility, transparency, and keeping track of your own work. I found a [tutorial for using RMarkdown](https://ourcodingclub.github.io/tutorials/rmarkdown/) from the Coding Club. 

For more intermediate users, I would recommend diving into the [Tidyverse!](https://www.tidyverse.org) The tidyverse is a collection of R packages designed specifically for data science. All packages work well together and share not only an underlying design philosophy, but also grammar and data structures. You may already be familiar with some of the packages included in the tidyverse: ggplot2 and dplyr. Easily install the complete tidyverse with: `install.packages("tidyverse")`.

R is great for data visualization (^ggplot2!). [Selva Prabhakaran has created a nice tutorial](http://r-statistics.co/R-Tutorial.html) for R and data visualization in R using ggplot2. This page also goes through many topics including linear regression, model selection, and time series data analysis.

Claus O. Wilke wrote an entire book called [Fundamentals of Data Visualization](https://serialmentor.com/dataviz/index.html) using RMarkdown, which he made open access as well as selling hard copies. This book is a great resource for learning about the basics of data visualization and how to avoid common problems like visualizing proportions or color choice.

Data Science
-----------------
The RafaLab has a number of excellent [teaching materials for using R for data science](http://rafalab.github.io/pages/teaching.html). They have lessons for many topics including, but not limited to:
  * R basics
  * Data visualization
  * Tidyverse
  * Machine learning in R
  * R for Life Sciences: 
    - High dimensional data analysis
    - Introduction to linear models and matrix algebra

If you are interested in improving your statistical abilities, here is a [Coursera course called "Improving your statistical inferences"](https://www.coursera.org/learn/statistical-inferences). 

The blog Eight to Late has a number of "gentle introduction" blog posts for various topics in data science, including [one for linear and logistic regression](https://eight2late.wordpress.com/2017/07/11/a-gentle-introduction-to-logistic-regression-and-lasso-regularisation-using-r/). Understanding linear and logistic regression are important topics, even if you do not intend to dive into deep learning and artificial intelligence. 

Learning a database language can be useful for data science. The Knight Lab has created a fun ["murder mystery" game to learn SQL](https://mystery.knightlab.com). They include an introductory lesson for beginners. Once you have completed the introduction (or if you already know SQL), you can jump into the murder mystery.  

Learning Python
----------------
CodeAcademy has [courses for learning Python](https://www.codecademy.com/catalog/language/python) that include the basics, analysing data, data visualization, and getting started with machine learning in Python.

There are a number of Python librarys that would be useful to learn as a computational biolgist. Here, I will list a few topics and related tutorials.
  * [NumPy for working with numerical data and matrices](https://numpy.org/devdocs/user/absolute_beginners.html)
  * [Pandas for fast and flexible data structures for data analysis](https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html)
  * [Scikit-learn tutorials for machine learning in Python](https://scikit-learn.org/stable/tutorial/index.html)
  * [SciPy, or Scientific Python, introduction and lessons](https://docs.scipy.org/doc/scipy/reference/tutorial/index.html)
  * [Biopython basics, practical computing for biologists](https://people.duke.edu/~ccc14/pcfb/biopython/BiopythonBasics.html)
  

There are a number of IDEs out there, but [Jupyter](https://jupyter.org) notebook seems to be the most popular for Python right now. [JupyterLab is a web-based IDE](https://jupyter.org/install.html) for [Jupyter notebooks](https://jupyter.org/install.html). In order to install Jupyter on your computer, you will need conda or pip, which may require some basic Python knowledge. 

Genomic Data Science
-------------------------
Genomic data science is a specialized field of data science that deals with next generation sequencing data. This [Coursera course on Genomic Data Science from Johns Hopkins University](https://www.coursera.org/specializations/genomic-data-science) covers topics from how genomic data are generated to the fundamentals of data analysis. Skills and topics included in this course: 
   * Next gen sequencing and genomic technologies
   * Genome analysis; DNA, RNA, and epigenetics
   * R: Bioconductor and R programming
   * Python: Biopython and python programming
   * Galaxy
  
[Bioconductor has also created many lessons](https://www.bioconductor.org/help/course-materials/) for learning about their various tools.
 
**High-dimensional data analysis** is becoming a necessary skill for computational biologists. High-dimensional data are basically any data set (think of a table of data with columns and rows, where rows are samples and columns are features of data, i.e. gene expression valuse or taxa abundances) where there are many, many more columns than rows. Another way you might see this, p >>> n (where n=number of samples and p=number of genomic features). The RafaLab resrouces that I mention above has lessons on this. There is also an [online course from Harvard](https://online-learning.harvard.edu/course/data-analysis-life-sciences-4-high-dimensional-data-analysis?category[]=84&sort_by=date_added&cost[]=free) that covers topics of high-dimensional data analysis such as: dealing with batch effects, dimension reduction, and PCA.

Dimensionality reduction is a topic that will touch most of our computational biology projects at some point. Anyone who has done a PCA has engaged in dimensionality reduction. Susan Holmes and Lan Huong Nguyen wrote a paper called ["Ten quick tips for effective dimensionality reduction"](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1006907#sec008) that I would recommend reading.

For beginning and more advanced Python users, [rosalind](http://rosalind.info/problems/locations/) has a bunch of bioinformatic challenges to help you learn about using Python for bioinformatics through problem solving.






  

To be continued...
--------
I will continue to update this post as I find more useful resources. 
