# cs436_assignment1
Implementation of decision trees using Information Gain and Variance impurity heuristics.

## Usage:
* execute the program using `python main.py {training-file} {validation-file} {test-file} {print?} {heuristic}`
  * the first three {file} parameters are the dataset files
    * paths for the files begin from the directory the program is in. Ex: test.csv for a file at that level, ./data/test.csv if it is in a folder named data
  * {print?} is either "yes" or "no" for printing out the decision tree
  * {heuristic} is either "0" for entropy-based or "1" for variance impurity

## Additional notes:
* I originally wrote this program on my local machine, which has Python 3. The remote servers use Python 2.7, so the `print` function could not take in a second parameter `end` to prevent newlines. This is the reason for the `__future__` import.
* As shocking as it may be, I am graduating this semester and have never been taught Python from this university, as my high school AP credit allowed me to skip CS110. Nonetheless, I understand how important the language is in this field, so I am taking the opportunity to teach it to myself this semester. I apologize if the code is a bit messy or unorganized, and I hope to improve my syntax with each project I use it for.
