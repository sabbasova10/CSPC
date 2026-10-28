# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup
Create the environment for a given lab:
conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc

---

## PW1 - Lab A: Reproducible Foundations

**What I built:**
- Two tests (test_rejects_negative_rate(), test_matches_law()) using pytest to check error raising and simulation correctness. 
- Speed test in speed.py using time.pref_counter() to track and compare execution time of loop and numpy vetsions of decay.  

**Speed comparison (loop vs NumPy):**
- loop : 3.4080823150000015 s
- numpy : 0.024006272999940848 s
- speed-up: 141.966323344252 x faster

**Tests:** all passing?
yes

**Conclusion:**
- All tests were passed and speed was calculated for two decay functions. I noticed that numpy is much more faster than simple loop because of the implementing function on whole array (vectorize) rather than iterating through each element in the loop, which makes it more effective to use for difficult calculations. Speed test may vary due to the laptop and OS condition in each moment.
- My repository was tested by my groupmate. All tests were passed, speed test was run.



## PW1 - Lab B: Data, Plotting and Automation

**What I built:**
- Program to plot two figures and save them as a .png file  for using matplotlib and numpy.
- Add simple automation script for Snakefile

**Showed Data**
- 2 figures with shared x and y axes.
- 1st figure is scatter graph with observed results
- 2nd figure is line plot with analicically calculated data
- From the graphs results are almost identical which confirms that law is working.

**Snakefile pipline**
- Snakefile defines input, output and terminal command to automate program execution and reduce unnecessary repetitions if no changes are made.

**Conclusion:**
- By using matplotlib the data can be visualized and studied more comprehensively for patterns, similarities and differences. Automation in this case helps to keep output up to date with the changes process (code, data) and facilitate the work by defining rules and steps of process. 



## PW2 - Lab A: Motion from Tracking Data

**What I built:**
- Program to analyse position and time data, find out velocity, acceleration and compare results with average data
- Snakefile for automation of two analysis processes (motion in 1D and 2D)

**Showed Data**
- 3 figures with shared x and y axes.
- 1st figure is line graph representing position over time
- 2nd figure is line graph representing velosity over time
- 3rd figure is line graph representing acceleration over time
- From the graph the amplification of noise after taking several derivatives is represented.

- 2 figures with path and speed in 2D motion

**Snakefile pipline**
- Targets to get two files by first rule, analyse 1D motion by the second rule, analyse 2D motion by the third rule.

**Conclusion:**
- The second order derivative amplifies the high-frequency measurements noise present in the position data, which create heavy variation in acceleration results.
- Standart deviation is high (28.71612), therefore mean (-8.57968) value is near standart g (-9.81), but not the same.
- When integration is used variation in results supperesed by sumation, so largest difference is just (0.78456)
- In conlusion, diffirentiation amplifies noice in measurements and feel errors, while integration suppress noise.



## PW2 - Lab B: Optimization in Chemistry

**What I built:**
- Program to optimize chemistry datasets via different optimizations techniques such as gradient descent, newton and SLSQP.
- Snakefile for automation of two analysis processes (kinetics and titration)

**Showed Data**
- Comparasion of 3 optimization techniques on simple and complex functions with different starting point.
- Curve-fitting optimization for a reaction rate (rate constant) with minimization of total error
- Optimization of equilibrium constant by minimizing amount of matter
- Titration equivalence point optimized by gradient. 

**Snakefile pipline**
- Targets to get two files by first rule, analyse kinetics.csv by the second rule, analyse titration.csv by the third rule.

**Conclusion:**
- All techniques agree (3.00) on simple functions with one minimum point. When function becomes more complex with several min/max points methods give different results.
- x0=0: Gradient descent = SLSQP = -1.3, Newton=0.17.
- x0=2: Gradient descent = Newton = 1.13, SLSQP=-1.3
- Newton method can show minimum when d2f > 0 (-5.65, x0=0) and maximum when 2df < 0 (9.35, x0=2) depending on starting point
- If function has several stationary points, Newton method goes until the nearest to the initial x0. It is due to the dg=0 which is used in this method. In Gradient descent slope going downwards, so the second starting point leads to the nearest minimum (it doesnt go upwards if needed).
- In kinetics k=0.26 which is fitted rate constant and optimized by curve-fitting, where squared error between measurement and theoretical value is minimized.
- Equilibrium point is optimized (x=0.66) and amounts are calculated(I2=0.34, H2=0.34, HI=1.33), by highliting eq. point.
- Equilibrium point is computed by taking largest gradient (50.0 ml) and pH jump is plotted.



## PW3 - Lab A: Data, Distribution, Testing, and Causation

**What I built:**
- Program to identify distribution of data in dataset.
- Snakefile for automation of figures generation from analysed data.

**Showed Data**
- Age is distributed approximatelly normally with more values on the left side (age < 70)
- Chortesol is skewed to the right (skew < 0, mean > median), there exist a standalone value. (W = 0.95; p = 5.91e-09)
- Resting blood pressure is skewed to the right (skew > 0, mean > median)
- Max heart rate is skewed to the left (skew < 0, mean < median)
- Q-Q ploting and p-value for resting blood pressure and max heart beat are varied noticingly from normal distribution. In age and cholesterol Q-Q plot approximatelly fit the normal distribution (minor head/tail differences) while p-value ensures it is not normal.

**After statistical check**
- After computation by Shapiro method all 4 dataframes were defined as not normal. 
- Age - W = 0.99; p = 6.07e-03
- Cholisterol - W = 0.95; p = 5.91e-09
- Resting blood pressure - W = 0.97; p = 1.80e-06
- Max heart rate - W = 0.98; p = 7.00e-05

**Snakefile pipline**
- Create distribution.png by the rule

**Conclusion:**
- The shape of heart.csv (Rows & Columns: (303, 14)).
- Distribution of all 4 parameters is not normal according t statistical analysis, even if in histogram it fits quite well.