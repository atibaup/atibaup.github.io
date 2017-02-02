---
layout: post
title: "ChileConCars: A Mixed Effects Model of Chilean used car prices - Part II"
date: 2017-02-03
---
(Note:) I'm new to Jekyll and haven't yet figured out how to escape parentheses \[duh!\]. So instead of parentheses I've been forced to use square brackets throughout...

I ended my [last post]({{ site.url }}/_posts/2016-11-22-chileConCars) commenting on the poorness-of-fit of the log-linear MEM model fitted to the Chilean used car [dataset]({{ site.url }}/assets/cleanCarData.csv). The residual vs. fitted plot seemed to indicate that there was an underlying non-linearity in the log-scale that the log-linear model wasn't able to capture. In this post I'll explore a polynomial spline model that does a better job at fitting the data, and I'll comment on the difficulty of estimating confidence intervals around the model parameters or its predictions.

Linear non-linearities
----------------------

 
