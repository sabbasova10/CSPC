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