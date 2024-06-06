# DLMDSPWP01-practical-assignment
source code for the practical assignment of course DLMDSPWP01 (IU University)

## Steps to install

- clone repository
- install dependencies ```make```
- open and run the Jupyter Notebook ```analysis.ipynb```
- to run the test ```make test```

## Jupyter notebook orientation

- Step1: data inspection through visualization: visualizes the given dataset(s) - train, test and ideal data - finally a combination of train and test data in one chart
- Step2: execute the analysis - uses the DataLoaders to load the source data, pump it to SQLite, calculates least-square-fit to identify the best fitting ideal functions for the training data, finally evaluates the test data against these functions

```
<spoiler>
🥳 Training data y1 fits best with ideal function y42
🥳 Training data y2 fits best with ideal function y41
🥳 Training data y3 fits best with ideal function y11
🥳 Training data y4 fits best with ideal function y48
</spoiler>
```

- Step3: Visualize best fitting ideal functions mapping to training data
![image](https://github.com/thomasreinecke/DLMDSPWP01-practical-assignment-code/assets/35994116/18f1b97c-bc6e-44e7-9653-cede2620fa2f)

- Step4: Visualize the mapping of the ideal functions against the given Test data
![image](https://github.com/thomasreinecke/DLMDSPWP01-practical-assignment-code/assets/35994116/36eddb3f-f689-43c1-bfa4-ed987dbc7ef1)
![image](https://github.com/thomasreinecke/DLMDSPWP01-practical-assignment-code/assets/35994116/85616fd0-be92-412e-9fdd-32e2477727e9)
![image](https://github.com/thomasreinecke/DLMDSPWP01-practical-assignment-code/assets/35994116/9efef14d-11de-4b0a-bdf2-5f3728f08ae4)
![image](https://github.com/thomasreinecke/DLMDSPWP01-practical-assignment-code/assets/35994116/b4fad066-f6cd-46dd-86f3-bc1c88c7c355)

## Additional task

Write the Git-commands necessary to clone the develop branch to your local PC. Imagine that you have
added a new function. Write all necessary Git-commands to introduce this project to the teams develop Branch.

```
git clone -b develop git@github.com:thomasreinecke/DLMDSPWP01-practical-assignment-code.git
cd DLMDSPWP01-practical-assignment-code.git

git checkout -b feature/cool-new-function

# write new code, save files

git add .
git commit -m "Added cool new function to find the world formula"

git push origin feature/cool-new-function

# now raise a Pull Request > which gets reviewed and merged
```
