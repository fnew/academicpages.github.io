---
title: 'The ACE Model: Estimating heritability with twins' data'
date: 2019-10-16
permalink: /posts/2019/11/blog_post_ACE_model/
tags:
  - ACE model
  - twins data
  - heritability
  - genetics
---

The ACE Model for Twins Studies
=================================
The twins structure of the dataset allows us to ask whether these microbial gene families are heritable. Monozygotic (MZ) twins share 100% of their DNA code, while dizygotic (DZ) twins share on average 50% of their DNA code. Any phenotypic differences between monozygotic (MZ) twins is theoretically due to the environment. Any excess in similarity between MZ twins over DZ twins must be due to genetics.

The common model to estimate heritability applied in twin studies is known as the ACE model. Twin studies using this model estimate how much the variation in a phenotype is due to additive genetic effects (A), the common environment (C), and the unique, random, environment (E). Structural equations modeling (SEM) partitions the variance of a phenotype into these three components using maximum likelihood methods. The SEM methods are implemented in the R- package OpenMx. 

Heritability
-------------
**Heritability (h2) is the proportion of variance of a phenotype explained by genetic variance (in a population).** Estimates of heritability range from 0 (no genetic influence) to 1 (totally controlled by genetics). Traits with h2 = 0 are things like spoken language, religion, political leanings. Genetic disorders like phenylketonuria (PKU) have a h2 near 1 because they are caused by a genetic mutation of a single gene. Many human traits are considered complex in that their heritability is somewhere between 0 and 1, indicating that genetic and the environmental factors both contribute to their variability. 

Heritability is *not* an estimate of what proportion of a trait is determined by genes and what proportion is determined by environment. For example, saying that height has a heritability estimate of 0.70 (for the record, it does not) does not mean that the height of one person is 70% caused by genes or genetic factors; it means that 70% of the variability in height in a population is due to the variance of genetic factors among the people of that population. 

Heritability also cannot tell you anything about which genes or which environmental factors are influencing a trait. It also does not provide any idea of how important those unknown factors are in determining a trait. 

And finally, high heritability does not necessarily mean that a trait is impossible to change. Hair color is highly heritable but it can be changed with hair dye, for example. Conversely, PKU is a highly heritable disorder and it is very difficult to change. This is important when thinking of features like the microbiome. The microbiome is easily alterable, so it is worth noting that heritability estimates do not indicate whether a trait is changeable.

Knowing how much influence genetics have on a trait is a useful starting point for research. Before performing genome-wide association studies, for example, it is useful to know how much variation in a trait we expect to be influenced by genetic variation. This allows us to know if the GWAS is capturing all genetic variation in the population or not.

Environmental Influences
-------------------------
Any influence other than DNA code that contributes to individual differences in a phenotype. Not to be confused with the traditional meaning of "the environment". 
Shared environment: any influences that make individuals who grow up together more similar. Parenting styles, home life, diet, socioeconomic status are examples of this.
Unique environment: any influences that make individuals who grow up together different. Children may have different friend groups, different hobbies, different injuries or illnesses. 

Biological Assumptions of the ACE model
-------------------------------------------
  * Findings from twins are generalizable to the rest of the population 
  * Assumes no GxE correlation or GxE interaction
  * No effect of chorion or amnion differences (in utero environment assumed to be identical)
  * Equal environment assumption
    * The environment affects MZ and DZ twins equally. Any excess in similarity between MZ twins over DZ twins must be due to genetics.
    * Evidence: mistaken zygosity, effect of physical similarity, effect of environment similarity

The Model
----------
The traditional ACE model assumes that phenotypes from each twin pair derive from a bivariate Normal distribution. Thus the model relies on the usual assumptions for normality. It is therefore necessary to transform your data and remove zeros in order to work with the ACE model. In the ACE model, phenotypes for monozygotic twins are assumed to have covariance,τ<sub>MZ</sub>, and phenotypes for dizygotic twins have covariance, τ<sub>DZ</sub>. All individuals have a common variance, σ<sup>2</sup>. The variance components A, C, and E are calculated using these covariances in the following way:

   τ<sub>MZ</sub> = A + C <br/>  
   
   τ<sub>DZ</sub> = ½A + C <br/>  
   
   σ<sup>2</sup> = A + C + E  

The ACE model uses the bivariate Normal distribution to model the phenotype of interest (Y<sub>i</sub>):

Monozygotic twins:<br/> 
![equation](https://latex.codecogs.com/gif.latex?%24%24%5Cbegin%7Balign*%7D%20%5Cbegin%7Bpmatrix%7D%20Y_%7B1%7D%5C%5C%20Y_%7B2%7D%20%5Cend%7Bpmatrix%7D%20%26%5Csim%20N%20%5Cbegin%7Bbmatrix%7D%20%5Cbegin%7Bpmatrix%7D%20%5Cmu_0%5C%5C%20%5Cmu_0%20%5Cend%7Bpmatrix%7D%5C%21%5C%21%2C%26%20%5Cbegin%7Bpmatrix%7D%20%5Csigma%5E2%20%26%20%5Ctau_%7BMZ%7D%5E2%5C%5C%20%5Ctau_%7BMZ%7D%5E2%20%26%20%5Csigma%5E2%20%5Cend%7Bpmatrix%7D%20%5Cend%7Bbmatrix%7D%5C%5C%20%5Cend%7Balign*%7D%24%24)

Dizygotic twins:<br/>
![equation](https://latex.codecogs.com/gif.latex?%24%24%5Cbegin%7Balign*%7D%20%5Cbegin%7Bpmatrix%7D%20Y_%7B3%7D%5C%5C%20Y_%7B4%7D%20%5Cend%7Bpmatrix%7D%20%26%5Csim%20N%20%5Cbegin%7Bbmatrix%7D%20%5Cbegin%7Bpmatrix%7D%20%5Cmu_0%5C%5C%20%5Cmu_0%20%5Cend%7Bpmatrix%7D%5C%21%5C%21%2C%26%20%5Cbegin%7Bpmatrix%7D%20%5Csigma%5E2%20%26%20%5Ctau_%7BDZ%7D%5E2%5C%5C%20%5Ctau_%7BDZ%7D%5E2%20%26%20%5Csigma%5E2%20%5Cend%7Bpmatrix%7D%20%5Cend%7Bbmatrix%7D%5C%5C%20%5Cend%7Balign*%7D%24%24)

Following the MLE calculation, we can get estimates for τ<sub>MZ</sub>, τ<sub>DZ</sub>, and σ<sup>2</sup>,  and can now solve for A, C, and E. The proportion of variance in a phenotype (i.e. a metagenomic gene abundances) attributable to additive genetics is A/A+C+E. 


Sources
--------
[Primer on heritabiltiy from the NIH](https://ghr.nlm.nih.gov/primer/inheritance/heritability) <br/>
[OpenMX](https://openmx.ssri.psu.edu)


