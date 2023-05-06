# Status report and development log for deliverable e) Experiment with other error checking packages or API
main function class: gingerErrorChecking.py

author: Peicheng Liu

## Deliverable purpose: 
The purpose of this deliverable is to experiment with other error checking modules and APIs such as Ginger API. ~~The team will conduct some research about accessible error checking modules and select one to be tested in the prototype.~~ The client provided with the team trail access to Ginger API, thus Ginger API is selected to be tested in the prototype. 

The team should produce similar output results as provided by the client in the repository resource folder (two .xlsx files containing the error checking results and corresponding details). 

The team also need to provide a report about the experiment, including the comparison between Ginger API and the existing error checking module (language-check-python), the pros and cons about the Ginger API and the suggestions the team can provide to the client. 

## Success Criterion/Test Plan: 
<input type="checkbox" disabled checked />
A working method to utilize all agreed modules (Single_Functions_by_Peicheng\gingerErrorChecking.py)

<input type="checkbox" disabled unchecked />
A written report analyse the pros and cons of different modules in various perspectives. (TODO)

<input type="checkbox" disabled checked />
Implement the method to the prototype. (Optional)
(documentchecker/views.py)

## Status report 
### 2023/04/05 
First attempt to implement the Ginger API in a standalone function. The function is save in Single_Functions_by_Peicheng\tmp.py temporarily. The method successfully sent the request but the server responses 'invalid key'. 
Will update with the client and see what is the problem.

### 2023/04/11
Talked to the client about the API key last weekends, and did some different try-outs about the request. The API key works in the test webserver provided by the Ginger guys but not in the standalone function. 

### 2023/04/12
The Ginger document is not consistent with the trial key, it turns out. we need to use 

    https://prevprod.gingersoftware.com/correction/v1/document

instead of

    https://sb-partner-services.gingersoftware.com/correction/v1/document

as the endpoint. 

### 2023/04/20 
Successfully implemented the Ginger API to check for document linguistic errors. The function takes around 10 seconds to check a document. A new python class 'gingerErrorChecking.py' is created to contain the function instead of the temporary file 'tmp.py'. 

### 2023/04/28
Successfully implemented the Ginger API to check for document linguistic errors with batch input. The input files provided by the client are all inputted to the function and the results are saved in the repository resource folder (See Single_Functions_by_Peicheng\Ginger_Error_Details.csv and Single_Functions_by_Peicheng\Ginger_Error_Stats.csv). 

The client provided input are processed so that only .doc and .docx files remains. Otherwise the input would be too large, and the function will run REALLY slow. 

### 2023/05/03 
The Ginger API is implemented to the prototype. The function is in the documentchecker/views.py class. The function is called when the user click the 'Complete' button in the frontend. The function will check the documents uploaded by the user and return the error checking results in the output folder (See Output\Ginger_Error_Stats.csv). 

### 2023/05/05
The team decided to use a pdf file as the output of the project. The time consumtion can be very long for the system to display the results in the frontend dashboard. In the future the program can email the results to the user instead of displaying the results in the frontend.

### 2023/05/06
The pdf generation plan is abondoned, instead, the team decided to use .html file as the output of the project. Since the output table easily exceeds the page size (See Output\Ginger_Error_Stats.html). 
An automatic generated graph is attached to the output file (See Output\Ginger_Error_Stats.png).
