# Status report and development log for deliverable b) metadata extraction
## Deliverable purpose:
  ### Objective:
  The goal of this project is to integrate Google Drive into our application, allowing users to download files from their Google Drive, update the file metadata, and save the modified file to our server. <br/>

  ### Key Features Implemented:<br/>
   Google Drive API integration for file listing and file download.<br/>
   Metadata update for the downloaded DOCX file using python-docx library.<br/>
   File upload and storage to the server using Django's In MemoryUploadedFile.<br/>

## Success Criterion/Test Plan:
  Several test google accounts was added and a basic function test was conduected to make sure the basic function work well in the whole project. In the future, an integrated test will be conducted when other parts of project is done. 
## Status report
### 2023/03/18
  Build the basic project framework, add the url section, and create the associated doc
### 2023/04/02
  Implement basic functions, implement Google drive api related calls, allow users to upload their documents to penwell via Google drive
### 2023/04/10
  Added Google picker, which provides users with a graphical interface to select files and improve user experience
### 2023/05/04
  merge this section into the main branch of your project to implement the functionality of this section
