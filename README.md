* Date : Nov, 11, 2018

* Author: Juan Lin

* Project: Insight data engineer program (Nov. session)

* Language: Python 3

* Problem statement
**************************************************************************************************************************************
A newspaper editor was researching immigration data trends on H1B(H-1B, H-1B1, E-3) visa application 
processing over the past years, trying to identify the occupations and states with the most number of 
approved H1B visas. She has found statistics available from the US Department of Labor and its Office 
of Foreign Labor Certification Performance Data. But while there are ready-made reports for 2018 and 
2017, the site doesn’t have them for past years.

As a data engineer, you are asked to create a mechanism to analyze past years data, specificially 
calculate two metrics: Top 10 Occupations and Top 10 States for certified visa applications.
***************************************************************************************************************************************

* Dataset
***************************************************************************************************************************************
https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf
***************************************************************************************************************************************

* Expected output
***************************************************************************************************************************************
This program creates two output files:
* top_10_occupations.txt: Top 10 occupatoins for certified visa applications
* top_10_states.txt: Top 10 states for certified visa applications 
****************************************************************************************************************************************

* Directory structure
****************************************************************************************************************************************
 ```
├── README.md 
├── run.sh
├── src
│     └──predCertified.py
├── input
│     └──h1b_input.csv
├── output
│     └──   top_10_occupations.txt
│     └──   top_10_states.txt
├── insight_testsuite
           └── run_tests.sh
               └── tests
                       └── test_1
                       |   ├── input
                       |   │   └── h1b_input.csv
                       |   |__ output
                       |   |   └── top_10_occupations.txt
                       |   |   └── top_10_states.txt
                       ├── test_2
                       ├── input
                       │   │   └── h1b_input.csv
                       |── output
                       |   |   └── top_10_occupations.txt
                       |   |   └── top_10_states.txt
```
******************************************************************************************************************************************

* Test your directory structure
******************************************************************************************************************************************
Under insight_testsuite directory, type ./run_tests.sh
******************************************************************************************************************************************

* File document
******************************************************************************************************************************************
The predCertified.py file is to find the desired items, for instance, certified state and certified job title, which 
are (WORKSITE_STATE, SOC_NAME). It then uses dictionaries to track the desired items and their values.  
After defining the function topRatio, it then uses three lists to track desired items, corresponding values and 
correponding ratio. They are then written into a .csv file through the function w2Txt.
*******************************************************************************************************************************************

* Corner cases
*******************************************************************************************************************************************
In ths project, four corner cases involving invalid input data were considered. 
* File not found. If the input data file is not found, the program will exit with an error. 
* CSV file empty. If the .csv file doesn't contain anything, the program will exit with an error. 
* Desired item field not found. If the desired columns are not found, the program will exit with an error. 
* Desired items values are empty.  If the desired items' values do not exist for a given row, that data will 
      be discarded and the program will continue. 
********************************************************************************************************************************************

* Performance
********************************************************************************************************************************************
This program works by using a Python dictionary as a histogram to keep track of the number of occurrances
of each unique entry in the desired column. The generation of this histogram requires one pass through the 
input dataset, which is O(n). Next the histogram is sorted, which is O(n log n) in the worst case (if every row 
was unique). Therefore, worst case time complexity of the program is O(n), which should scale well to large
data sets. The statistics for the state and the occupation are computed seperately, requiring two full
passes though the input data. This separation was intentional to facilitate easy re-use of the code, but
both could be combined into one pass easily if better performance is necessary. 
*********************************************************************************************************************************************

* Contact Information
*********************************************************************************************************************************************
Please send an email to jlinncsu@gmail.com if you have any questions.
*********************************************************************************************************************************************
