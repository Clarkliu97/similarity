import requests
import json
from docx import Document 
import os 
import olefile

# Replace YOUR_API_KEY with your actual API key from Ginger Software
API_KEY = "917c943b-ed2f-41b1-a251-1303d17dc515" 

# Construct the request URL and headers
url = "https://prevprod.gingersoftware.com/correction/v1/document?apiKey=" + API_KEY + "&lang=UK"

#  Content-Type: text/plain
headers = {"Content-Type": "text/plain"}

# target directory of the doc files
target_directory = "Single_Functions_by_Peicheng\Asset" 

def main(): 
    # Read all .doc or .docx files in the target directory recursively and store the file names in a list 
    file_list = [] 
    for root, dirs, files in os.walk(target_directory): 
        for file in files: 
            if file.endswith(".doc") or file.endswith(".docx"): 
                file_list.append(os.path.join(root, file)) 

    # # print all the file names in the list
    # for i in range(len(file_list)): 
    #     print(i, " ", file_list[i])

    # Read the content of each DOC or DOCX file in the list 
    docTexts = []
    for i in range(len(file_list)): 
        extension = os.path.splitext(file_list[i])[1]
        try: 
            if extension == ".docx": 
                with open(file_list[i], "rb") as f: 
                    doc = Document(f) 
                    docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)
                    docText = docText.encode('utf-8')
            elif extension == ".doc": 
                docText = get_doc_text(file_list[i])
                docText = docText.encode('utf-8')
        except: 
            print("Error reading file: ", file_list[i]) 
            docText = ""
        docTexts.append(docText)

    if len(docTexts) == len(file_list): 
        print("Successfully read all files in the target directory.")

    # Send the HTTP POST request to the API endpoint
    # test with 5 files
    five = 5 if len(docTexts) > 5 else len(docTexts)
    for i in range(five): 
        response = requests.post(url, headers=headers, data=docTexts[i])
        num_errors = 0
        # Check if the request was successful
        if response.status_code == 200:
            try:
                # Parse the response JSON object
                result = json.loads(response.text)
                result = json.dumps(result, indent=2)
                # print(result)
                # write response text to json file
                with open('Single_Functions_by_Peicheng\ginger_error_tmp.json', 'w') as f:
                    f.write(result)
                    f.close()

                with open('Single_Functions_by_Peicheng\ginger_error_tmp.json', 'r') as f:
                    result = json.load(f)
                    
                # Extract the errors from the response
                if "GingerTheDocumentResult" in result:
                    documentResult = result["GingerTheDocumentResult"]
                    errors = documentResult["Corrections"] 
                    for error in errors: 
                        # print(error)
                        categoryId = error["TopCategoryId"] 
                        # print(categoryId)
                        start = error["From"]
                        end = error["To"]
                        num_errors += 1
                else:
                    print("No errors detected.")
            except json.decoder.JSONDecodeError as e:
                print(f"Failed to parse JSON response: {e}")
        else:
            print(f"Request failed with status code {response.status_code}.")
        print(f"Number of errors in file {i}: {num_errors}")




if __name__ == "__main__":
    main()

def get_doc_text(file):
    import tempfile
    tempf, tempfn = tempfile.mkstemp(suffix='.doc')
    for chunk in file.chunks():
        os.write(tempf, chunk)
    from subprocess import Popen, PIPE
    cmd = ['antiword', tempfn]
    p = Popen(cmd, stdout=PIPE)
    stdout, _ = p.communicate()
    text = stdout.decode('ascii', 'ignore')
    return text