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