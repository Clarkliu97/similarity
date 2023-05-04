import requests
import json
from docx import Document

# Replace YOUR_API_KEY with your actual API key from Ginger Software
API_KEY = "917c943b-ed2f-41b1-a251-1303d17dc515"

# Replace DOCX_FILE_PATH with the path to your DOCX file
DOCX_FILE_PATH = "Single_Functions_by_Peicheng\Asset\Feminist Literary theory.docx"

# Read the content of the DOCX file
with open(DOCX_FILE_PATH, "rb") as f:
    doc = Document(f)
    docText = '\n\n'.join(paragraph.text for paragraph in doc.paragraphs)

# Construct the request URL and headers
url = "https://prevprod.gingersoftware.com/correction/v1/document?apiKey=" + API_KEY + "&lang=UK"

#  Content-Type: text/plain
headers = {"Content-Type": "text/plain"}

# # Construct the request body as a plain text string
# data = { "apiKey": API_KEY, "lang": "UK", "text": docText }

print(docText.encode('utf-8'))

# Send the HTTP POST request to the API endpoint
response = requests.post(url, headers=headers, data=docText.encode('utf-8'))

# Check if the request was successful
if response.status_code == 200:
    try:
        # Parse the response JSON object
        result = json.loads(response.text)
        result = json.dumps(result, indent=2)
        # print(result)
        # write response text to json file
        with open('Single_Functions_by_Peicheng\ginger_error.json', 'w') as f:
            f.write(result)
            f.close()

        with open('Single_Functions_by_Peicheng\ginger_error.json', 'r') as f:
            result = json.load(f)
            
        # Extract the errors from the response
        if "GingerTheDocumentResult" in result:
            documentResult = result["GingerTheDocumentResult"]
            errors = documentResult["Corrections"] 
            for error in errors: 
                # print(error)
                categoryId = error["TopCategoryId"] 
                print(categoryId)
                start = error["From"]
                end = error["To"]
        else:
            print("No errors detected.")
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to parse JSON response: {e}")
else:
    print(f"Request failed with status code {response.status_code}.")
    #  write response text to html file
    with open('Single_Functions_by_Peicheng\ginger_error.html', 'w') as f:
        f.write(response.text)
        f.close()

