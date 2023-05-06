# Status report and development log for deliverable b) metadata extraction 
main function class: metadata_extraction.py
author: Peicheng Liu

## Deliverable purpose: 
The purpose of this delivery is to increase the reliability of user input. According to the user story map, when users upload their documents, especially from their school drives, it is likely that some documents which are not written by the student will be included. As this project should reflect on the student writing only, the system should not count errors belonging to the teacher or other people. By excluding these files from the analysis, the reliability of the error-student link is enhanced.  

## Success Criterion/Test Plan: 
~~At least 70% of the files can be distinguished by the algorithm properly; ready to be integrated to the prototype or ready to be called by other class.~~

~~Test against all files provided by the client. Will need client to provide correct labels for the files. 70% correct rate should suffice.~~

The algorithm will be test against the resource data provided by the client. No more than 10% files with inconsistence author vs last modifier can be fed into next steps, ready to be integrated to the prototype or ready to be called by other class. 

Will provide a rate of removal to the client. In theory, if we determine the files with inconsistence author vs last modifier are not reliable, then the rate of removal should be able to benchmark how much more accuracy was increased by the algorithm. 

The equation for the removal rate is: 

    removal rate = (number of files with inconsistence author vs last modifier) / (total number of files)

## Status report
### 2023/03/16
Standalone version of the metadata extraction tool is created. It can now extract metadata from a single file. The file type must be either .docx or .doc. The metadata extracted includes: Creator, Created Time, Last Modifier, Last Modified Time. 

### 2023/03/20
The tool can now extract metadata from a folder, recursively. ~~The folder must contain only .docx or .doc files~~. It now write the metadata to a sqlite database. 

### 2023/03/21
Walked through the existing prototype code, the method used for metadata extraction is very simialr to the standalone function. The implementation of backend should be very easy.

### 2023/03/25
The tool can now compare the Creator and Last Modifier of a file. And it can output the comparation result as a boolean value. The sqlite database is removed from the standalone function, use a csv file instead for easier demo illustration. 

### 2023/03/28
he function now also record the file name in the csv file. 

### 2023/04/05
The functions is now integrated to the prototype. The metadata extraction is now a part of the backend. Excluding inconsistent files from the analysis. 
Updated documentchecker/serializers.py and documentchecker/utils.py. See commit log for more details. 
