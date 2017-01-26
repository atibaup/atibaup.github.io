---
layout: post
title: "Mixing Mixed Effect Models and Chilean used car prices"
date: 2017-01-24
---

As some of you may know, my wife and I recently spent a few months [traveling in South America](http://properaestacio.wordpress.com). We did the southernmost part of our trip - Chile and Argentina's Patagonia - driving a car, which we bought in Santiago, Chile. As a sidenote, Chile happens to be the only South American country at the time of writing this post that [is somewhat friendly to foreigners buying cars and bringing them out of the country](http://practicingforretirement.com/index.php/buy-a-car-in-chile/).

Buying a used car is always a risky business, particularly in a foreign country that you don't know well. One of the obvious potential risks is that of overpaying, and since we had a lot of time to kill in Santiago while we were waiting for a strike to end, I decided to do a little bit of research on used car prices for the makes and models we were interested in.

What started like a small spreadsheet project ended up becoming a little more involved: I built a web scraper on R to download the prices of the listings from a couple of chilean websites, as well as a small shiny app to display and filter the results that were more relevant \(you can find the whole project's source code here: [github.com/atibaup/chileConCars](https://github.com/atibaup/chileConCars).\)

In this blog post, I wanted to share some of the analysis that I did on the used car data, which turned out to be a pretty good used case for a class of models that I like: Mixed Effect Models.

Dataset
-------

The [dataset]({{ site.url }}/assets/cleanCarData.csv), which we obtained by scraping [chileautos.cl](http://www.chileautos.cl) and [yapo.cl](http://www.yapo.cl), contains 4213 samples of used cars with 17 features for each sample: 
"Nombre", "Año", "Fecha", "URL", "Código", "Kilómetros", "Precio", "Precio.anterior", "Tipo.de.vehículo", "Combustible", "Transmisión", "Edad", "Precio.USD", "Kilómetros.miles", "make", "model", "source".

The breakdown of samples by make and model is shown below. It's not surprising to see some of expensive models at the end of the list, but I was suprised by the huge lead in popularity that Suzuki's got over its competitors. Or is it just that everyone's trying to sell their Suzukis while other makes' owners keep their cars throughout their lifetime?

Suzuki GrandNomade | Suzuki GrandVitara | Honda CR-V | Toyota 4Runner | Nissan X-Trail | Mitsubishi Montero | Nissan Pathfinder | Toyota LandCruiser
:---: | :---: | :---: | :---: | :---: | :---: | :---: | :---:  
37.9 %|16.8% | 11.9% | 8.8% | 8.2% | 7.5% | 5.7% | 3.1%

In Chile, used cars tend to have automatic transmission, but manual cars are not far behind:

Automático | Manual |  NA's
:---: | :---: | :---: 
50.2%  | 40% |9.7 %

And unsurprisingly, Gas \[Bencina\] is a lot more popular than Diesel.

Bencina | Diesel | Gas | Otros
:---: | :---: | :---: | :---:
95.1% | 4.7% | 0.1% | 0.0% 

We can also look at the statistics of some of the features of interest, like the mileage \[Kilómetros\], the age \[Edad\] and the price in USD. The next figure shows the histograms and density estimates for each of these variables, segmented by model \[the row order for each column is descending in the mean of the column's variable\]:

![]({{ site.url }}/assets/summary.png)

We can see that most used cars have around 100,000km under their hoods, and their ages are concentrated around the 10 years mark. Not surprisingly, models that are well-nown to be very robust like the Mitsubishi Montero or the Toyota Landcruiser display a larger mileage and age spread, with some of the listings running well over 300,000kms. So if you're thinking about driving 7 times around the world at the equator, you may want to consider one of those two!

The price statistics above also give a sense of the type of car that one can get for a given budget. For example, for a 10,000USD investment, we're better off looking for a Suzuki Grand Nomade or a Honda CR-V than a Toyota Land Cruiser or a Toyota 4Runner, since the number of listings for the latter two for that price range is quite small. 

Perhaps the most interesting feature is the bi-modality in the distribution of prices for some of the models \[e.g. Pathfinder, 4Runner\], which is largely explained by the bi-modality in the distribution of ages of the same segment. 

Estimating depreciation rates via  Mixed Effect Models on R
-----------------------------------------------------------

Since our main motivation for purchasing a car was to travel with it, we knew that we would be selling at the end. A natural question to ask then is how much will the car depreciate by the time we sell it, since this can inform our decision to choose one model or the other. We can try to estimate the \[listing price\] depreciation rate from the listing data *for each car model* via a simple additive regression model of the form:

$p =  f_1(a) + \sum_{j>1} f_j\left(x_j\right)  + \epsilon$  

where $p$ is the listing price, $a$ is the age, the $x_j$'s are other relevant price-predicting features, $f_j$ are regression functions, $epsilon$ is i.i.d. error. Assuming that the variables $x_j$ do not depend on the age variable $a$,  we can obtain an estimate of the depreciation rate for each model as:

$\frac{\partial p}{\partial a} = \frac{\hat{f}_1}{\partial a} $

where $\hat{f}_1$ is the estimate of the regression function modeling the dependency between price and age.

This approach has the problem that it would treat each car model independently, which given the scarcity of samples for some of the car models \[see Toyota Land Cruiser or Nissan Pathfinder's in the table above\] may not be a great idea. For example the depreciation rate for the Pathfinder would be estimated with only 130 samples, while the GrandNomade's would be estimated with nearly 1600 samples, without leveraging the fact that all of these samples share a commonality: they all correspond to SUV type cars, with 4 wheels, one steering wheel, and so on and so forth.  

An alternative to this naive approach of treating each car model indepentently, is to explicitly 
introduce a mechanism to pool information from the samples across all car models. One such mechanism is provided by Mixed Effect Models, which we will consider here in a simplified linear model first. In this model, the response $p$ is a linear function of the age and other variables,

$$

but the parameter corresponding to the age 
 


Handling non-linearity
----------------------


Conclusions
-----------  
