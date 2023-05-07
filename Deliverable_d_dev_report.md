# Status report and development log for deliverable d) document classification with GPT 
main function class: views.py
author: Jiayong Zhu & Jingsong Yan

## Deliverable purpose: 
The purpose of this deliverable is to classify documents by genre and course. Also, according to our user story map, we may also visualize the type of linguistic errors by genre and subject based on this.
## Success Criterion/Test Plan: 


The algorithm will be test against the resource data provided by the client. No more than 10% of the documents without a label can be fed into next steps. If the client provides correct labels to each document, at least 70% of the files can be correctly labelled by the algorithm; ready to be integrated to the prototype or ready to be called by other class. The quality of this deliverable should at least be aligned with P Performance Criterion in Team Charter. 


## Status report
### 2023/04/13
Research report finished, prepare to implement method by using Chat-GPT.
### 2023/04/17
By using openAI api, we first create a method which can classify our given document by genre. And the test result seems good.
### 2023/04/26
Re-construct this method, since our method can only classify document by genre. However, the performance of our test result seems not good this time. By checking some documents that are classify wrong, we find some documents are ambigorous, so that our API tool does not enable a good classification.
### 2023/05/03
This tool now can read files, and classify files based on our given genres and courses. Also, Jiayong and I have done some testing, however, the testing result still perform not good enough. By human inspection, we believe that some genres are indeed difficult to distinguish from others. In conclusion, we have achieved this deliverable, and we also believe that the performance of this tool will improve as the upgrade of GPT.

