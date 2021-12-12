# Life beyond Earth

### Overview:
Life beyond the Earth has always been a fascinating quest for scientists. Roughly 1.2% out of an approximate 5000 exoplanets have been found to be in the “habitable zone [1]” in our observed universe, yet there exists a question on whether these planets could actually host life. At the same time, there are organisms on earth – the extremophiles, that can survive under extreme conditions these exoplanets [2] have to offer. Our study analyzes these planets and examines the survival rate of extremophiles [3] on these planets.

Here are the hypotheses we found fit to explore extremophiles on exoplanets:

### Hypothesis 1: All exoplanets that fall in the habitable zone of their solar system posses earth-like conditions and vice-versa.

---
1. Planets that orbit around a star outside the solar system.
2. Orbital region around a star in which planets can posses liquid on its surface and possibly posses life.
3. Planets whose earth similarity index is 0.6 and above - A quantitative measure of departure from a reference state, usually on a scale from zero to one.

Formulae to calculate ESI:

![](https://github.com/Saahil87/2021Fall_finals/blob/main/visualizations_files/New.png?raw=true)

#### <u>Step 1:</u>
Using the above formulae calculate ESI of each planet using 4 planetary properties - 
1. Radius
2. Density
3. Escape Velocity
4. Surface Temperature
for each exoplanet in the database.

#### <u>Step 2:</u>
Get the list of exoplanets that fall in the habitable zone by calculating the planet distance from it's sun and verifying if it lies in between the habitable max radius and min radius of that sun.

#### <u>Step 3:</u>
Identify the type of habitability as 
1. Conservative - 
   0.2 < Planet Radius < 1.5
   0.1 < Planet Mass < 5.0
2. Optimistic - 
   1.5 < Planet Radius < 2.5
   5.0 < Planet Mass < 10.0

![](https://github.com/Saahil87/2021Fall_finals/blob/main/visualizations_files/visualizations_7_0.png?raw=true)

#### <u>Step 4:</u>
Identify the overlap between planets that lie in the habitable zone and the planets that are earth-like using step 1 and 2:

![](https://github.com/Saahil87/2021Fall_finals/blob/main/visualizations_files/visualizations_10_0.png?raw=true)

#### <u>Step 5:</u>
Send all the common and earth like planets as an input for Hypothesis 2.

#### <u>Step 6:</u>
Plot all the planets with their sun (its habitable zones) and planet orbits.

![](https://github.com/Saahil87/2021Fall_finals/blob/main/visualizations_files/habitable_zone.png?raw=true)

---


### Hypothesis 2: If any of the exoplanets possesses similar conditions in which an Extremophile can survive, then those planets could potentially host life.

---



#### <u>Step 1:</u>
After the analysis from hypothesis one, use all potentially habitable planets to identify extremophiles that can survive extreme temperatures, pressures, and radiation respectively.

#### <u>Step 2:</u>
Plotting all surviving Extremophiles 

##### Extremophiles surviving extreme temperatures

![](https://github.com/Saahil87/2021Fall_finals/blob/main/visualizations_files/visualizations_21_0.png?raw=true)

##### Extremophiles surviving extreme pressures

![](https://github.com/Saahil87/2021Fall_finals/blob/main/visualizations_files/visualizations_23_0.png?raw=true)

##### Extremophiles survivng extreme radiation

![](https://github.com/Saahil87/2021Fall_finals/blob/main/visualizations_files/visualizations_25_0.png?raw=true)

#### <u>Step 3:</u>
Identifying overlap between all survivng extremophiles obtained in step 1

![](https://github.com/Saahil87/2021Fall_finals/blob/main/visualizations_files/visualizations_30_0.png?raw=true)




[1] Habitable Zone - the orbital region around a star in which an Earth-like planet can possess liquid water on its surface and possibly support life.

[2] Exoplanets - Planets that orbit around other stars are called exoplanets.

[3] Extremophiles - a microorganism, that lives in conditions of extreme temperature, acidity, alkalinity, or chemical concentration.

### References:
https://www.frontiersin.org/articles/10.3389/fmicb.2019.00780/full

https://iopscience.iop.org/article/10.3847/1538-4357/aae36a/meta

https://www.liebertpub.com/doi/pdfplus/10.1089/ast.2010.0592?casa_token=WeRF3fb2GWAAAAAA:dKP0925At8zc3nneqk_q1Az55YN2Jq9vR4QzM5CcoFRghpAJ8yWXdBRrinKr9JTqblCfUGcg8ZiNkwpu
