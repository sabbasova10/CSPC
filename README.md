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


## PW3 - Lab B: Data, Distribution, Testing, and Causation

**What I built:**
- Continue the program to statistical analysis of heart desease data to investigate correlations.
- Program to analyse a chemical exposure dataset to investivate correlation and causation.
- Snakefile for automation of figures generation from analysed data.

**Showed Data**
- mannwhitneyu() method was selected because all the columns are not distributed normally. U-static=5806.50; p-value=1.86e-13

- By this result thalach (max heart beat) groups (significantly differ), null hypoteses regected.

- Desease: mean=139.26; SE=1.92; CI=[135.43,143.09]

- Healthy: mean=158.38; SE=1.50; CI=[155.38,161.38]

- Indeed 2 groups are different and have a slight diversity in values of mean (se_healthy = 1.5, se_desease = 1.92)

- r=-0.3938, p=1.11e-12. Corilation between age and thalach is negative and moderate relationship.

- Cadmium looks like the cause of cancer because it corelates more (Benzen: r=0.3847,
Cadmium: r=0.8800).

- Relationship between pollution index and cancer is strong (r=0.8951, with age r=-0.0338) so we take this colunm to restric two others.

- Real cause is Benzene (corelation after restriction of set by pollution index r=0.6979).

-  Entropy of target: 1.00. Meaning that values unpredictible.


**Snakefile pipline**
- Create distribution.png, barchart.png and corilation.png by the rules

**Conclusion:**

-Since values are not normal the selected method is Mann-Whitneyu U test (non-parametric test)
- p-value (1.86e-13) is much smaller than 0.05, so the null hypothesis of no difference between the groups(health and desease) is rejected.

- Patients with heart disease have a lower mean maximum heart rate than healthy individuals in this dataset by statistical test and confidence intervals.

- Age and maximum heart rate have a statistically significant, moderate negative correlation (r=-0.3938). Older individuals tend to have lower maximum heart rates, although age alone does not fully explain the variation in maximum heart rate.

- At fisrt glance causation is determined as Cadmium due to strong correlation (r=0.8800).

- However real causation is determined as benzene. This happens because one feature can correlate better with another in general but not at every individual set. So strong corilation doesnt mean causation.

- Standart restrictions
Benzen: r=0.6979, p=1.15e-30
Cadmium: r=0.3132, p=5.99e-06

- Narrow restrictions
Benzen: r=0.6676, p=1.09e-13
Cadmium: r=-0.0367, p=7.23e-01

- The target variable has high entropy, meaning that its categories are difficult to predict from their overall frequencies alone. However, entropy measures uncertainty in the category distribution; it does not mean that every individual outcome is unpredictable when other features are considered.


## PW4 - Lab A: Concrete Compressive Strength (Supervised Learning)

**Dataset Citation: Yeh, I-Cheng (1998). Concrete Compressive Strength, UCI Machine Learning Repository (ID: 165).**

**What I built:**
- fetch_concrete.py downloads the UCI Concrete Compressive Strength dataset, renames columns, inspects metadata/variables, and saves data/concrete.csv .

- sessionA.py cleans the data, performs linear and polynomial regression, trains KNN and Decision Tree classifiers, evaluates classification metrics and probability thresholds, compares feature importance methods, and tests physics-informed features.

- Plots and tables in results/ (corelation.png, linear_residuals.png, poly_degrees.png, knn_sweep.png, tree_depth.png, feature_importance.png, and A_metrics.csv).

**Showed Data**

- **A1** 
  - cement kg/m^3, slag kg/m^3, ash kg/m^3, water kg/m^3, superplastic kg/m^3, coarse_agg kg/m^3, fine_agg kg/m^3, age day, strength MPa — Target

- **A2**
- 25 duplicate rows and 0 missing values (1030 -> 1005 unique rows)
- df.describe() shows coarse_agg, fine_agg, and cement span hundreds of kg/m^3, whereas superplastic and age span much smaller numerical ranges.
- strength vs. cement shows a weak-to-moderate positive trend with wide scatter (r = 0.4883).
- strength vs. age shows a strong non-linear (logarithmic) curve that rises rapidly in early curing days and levels off later (r = 0.3374).

- **A3**
- 80/20 split (random_state=42): 
Training set size: X=(804, 8), y=(804,)
Test set size:     X=(201, 8), y=(201,).

- **A4**
- Equation: y_hat = -23.39_MPa + 0.1167 x_cement_MPa_per_kg + 0.0981 x_slag_MPa_per_kg + 0.0846 x_ash_MPa_per_kg - 0.1314 x_water_MPa_per_kg + 0.3315 x_superplastic_MPa_per_kg + 0.0155 x_coarse_agg_MPa_per_kg + 0.0206 x_fine_agg_MPa_per_kg + 0.1106 x_age_day

- intercept in MPa, ingredients in MPa per kg/m^3, age in MPa per day.

- A4 Performance Metrics

| Metric | Value |
| :--- | :---: |
| Train RMSE | 10.002 MPa |
| Test RMSE | 11.191 MPa |
| Test MAE | 8.895 MPa |
| Train R2 | 0.610 |
| Train Adj R2 | 0.606 |
| Test R2 | 0.580 |

- Plotting test residuals against log(age) shows residuals concentrated on the positive side at intermediate ages and negative at extremes rather than randomly scattered around zero.

- **A5**
- A5) Polynomial Regression Comparison

| degree | p | train_RMSE | test_RMSE | test_MAE | train_R2 | train_adj_R2 | test_R2 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 8 | 10.002 | 11.191 | 8.895 | 0.610 | 0.606 | 0.580 |
| 2 | 44 | 6.989 | 8.308 | 6.220 | 0.809 | 0.798 | 0.769 |
| 3 | 164 | 4.396 | 5.952 | 4.501 | 0.925 | 0.905 | 0.881 |
| 4 | 494 | 2.334 | 39.410 | 10.028 | 0.979 | 0.945 | -4.206 |

- At degree 4, features expand to p = 494 (more than half of n = 804 training rows), causing test R^2 to become strongly negative and test RMSE to spike while training R^2 (adjusted) remains high.

- **A6**
- Class proportions: 0 (< 40 MPa = 0.6418 (64.2%), 1 (>= 40 MPa = 0.3582 (35.8%).

| K | train_acc | test_acc |
| :---: | :---: | :---: |
| 1 | 0.997512 | 0.830846 |
| 3 | 0.934080 | 0.800995 |
| 5 | 0.906716 | 0.815920 |
| 7 | 0.893035 | 0.835821 |
| 15 | 0.848259 | 0.825871 |
| 25 | 0.840796 | 0.805970 |
| 51 | 0.804726 | 0.781095 |
| 101 | 0.757463 | 0.736318 |

Chosen K = 7
Test accuracy with StandardScaler:    0.8358
Test accuracy without StandardScaler: 0.8209

5-split test accuracies (random_state 0..4): [0.801, 0.8507, 0.8209, 0.8358, 0.806]
Mean: 0.8229 | Std: 0.0185 | Range (max - min): 0.0498.

- Decision Tree (tree_depth.png):

| max_depth | n_leaves | train_accs | test_accs | gap |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 2 | 0.7550 | 0.7015 | 0.0535 |
| 2 | 4 | 0.7550 | 0.7015 | 0.0535 |
| 3 | 8 | 0.8396 | 0.7960 | 0.0435 |
| 4 | 16 | 0.8694 | 0.8259 | 0.0435 |
| 5 | 26 | 0.8893 | 0.8458 | 0.0435 |
| 6 | 38 | 0.9303 | 0.8408 | 0.0896 |
| 8 | 61 | 0.9726 | 0.8557 | 0.1169 |
| None | 80 | 0.9975 | 0.8806 | 0.1169 |

- Top two levels of tree (max_depth=4):
Age is checked at the 42 days, then cement is checked on 257.7 then water on 156.2
if cement > 257.7 then superplastic is checked at 0.95

If age > 42, then superplastic is checked on 6.45 then fine_agg on 749.55
if superplastic >  6.45 then cement is checked on 203.35

- **A7**

| model | TP | FP | FN | TN | accuracy | precision | recall | f1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| KNN (K=7) | 54 | 15 | 18 | 114 | 0.8358 | 0.7826 | 0.7500 | 0.7660 |
| Decision Tree (max_depth=4) | 58 | 21 | 14 | 108 | 0.8259 | 0.7342 | 0.8056 | 0.7682 |

- Threshold change for KNN (K=7)

| threshold | TP | FP | FN | TN | precision | recall |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0.3 | 61 | 23 | 11 | 106 | 0.7262 | 0.8472 |
| 0.5 | 54 | 15 | 18 | 114 | 0.7826 | 0.7500 |
| 0.7 | 39 | 11 | 33 | 118 | 0.7800 | 0.5417 |
| 0.9 | 18 | 1 | 54 | 128 | 0.9474 | 0.2500 |

- **A8**
- A8) Feature Importance Comparison

| feature | raw_coef | std_coef | tree_imp | perm_knn_f1 | perm_knn_std | perm_tree_f1 | perm_tree_std |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| cement | 0.1167 | 12.1188 | 0.2895 | 0.1646 | 0.0359 | 0.1932 | 0.0310 |
| slag | 0.0981 | 8.4373 | 0.0199 | 0.0552 | 0.0208 | 0.0000 | 0.0000 |
| ash | 0.0846 | 5.4395 | 0.0000 | 0.0159 | 0.0160 | 0.0000 | 0.0000 |
| water | -0.1314 | -2.8279 | 0.0371 | 0.0680 | 0.0247 | 0.0098 | 0.0105 |
| superplastic | 0.3315 | 1.9708 | 0.1929 | 0.0663 | 0.0316 | 0.1706 | 0.0289 |
| coarse_agg | 0.0155 | 1.1990 | 0.0080 | 0.0384 | 0.0178 | 0.0000 | 0.0000 |
| fine_agg | 0.0206 | 1.6699 | 0.0861 | 0.0808 | 0.0250 | 0.0663 | 0.0176 |
| age | 0.1106 | 6.8945 | 0.3666 | 0.1757 | 0.0335 | 0.1338 | 0.0304 |

- raw coefficients differ in ranking from standardized coefficients due to differing measurement units, while standardized coefficients, tree importances, and permutation importances all rank cement and age among the top drivers (with slag ranking 2nd in standardized linear coefficients, and superplastic ranking 3rd in tree and permutation importances while water has a negative linear effect and smaller tree/permutation scores).

- **Bonus**
- Bonus) Physics-Informed Features

| model | p | test_R2 |
| :--- | :---: | :---: |
| Linear + log(age) | 8 | 0.804 |
| Linear + log(age) + w/b | 8 | 0.806 |

- replacing age with ln(age) and water with w/b = water/(cement + slag + ash) keeps p = 8 features while raising test R^2 well above plain linear regression.

**Conclusion**

- Duplicate rows must be removed before splitting so identical examples do not leak across train and test sets and artificially increase performance. 
- Large scale differences across features make StandardScaler essential for distance-based models like KNN and polynomial numerical stability.

- The systematic curved pattern in linear residuals confirms a non-linear relationship, meaning plain linear regression underfits. 
- Degree 3 polynomial regression is optimal because it minimizes test error and the train–test gap.
- Degree 4 severely overfits because p = 494 approaches n = 804, and training R^2 (adjusted) fails to warn against this because it is computed only on training data.

- K = 7 balances bias and variance in KNN, while max_depth = 4 for the Decision Tree avoids the overfitting of an unpruned tree (None) and keeps the rules human-readable. The top tree splits on age, cement, and water align with concrete curing physics.

- On a construction site, a False Positive (FP) is the dangerous mistake because weak concrete (< 40 MPa) would be approved for structural use; precision controls it. 
- Raising the decision threshold to 0.7 (or 0.9) reduces FP and increases precision, at the cost of lower recall (more False Negatives, meaning some acceptable concrete are rejected or require further testing).

- All importance methods agree that age, cement, and water drive predictions, matching engineering principles, though high statistical importance alone does not establish causation without controlled experiments. 

- Encoding domain physics ln(age) and w/b ratio achieves high accuracy with only p = 8 features, proving that physical insight can outperform blind high-degree polynomial complexity.