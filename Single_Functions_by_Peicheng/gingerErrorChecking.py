import requests
import json
from docx import Document 
import os 
import csv

# Replace YOUR_API_KEY with your actual API key from Ginger Software
API_KEY = "917c943b-ed2f-41b1-a251-1303d17dc515" 

# Construct the request URL and headers
url = "https://prevprod.gingersoftware.com/correction/v1/document?apiKey=" + API_KEY + "&lang=UK"

#  Content-Type: text/plain
headers = {"Content-Type": "text/plain"}

# target directory of the doc files
target_directory = "Single_Functions_by_Peicheng\Asset\Student A (2019-2021)" 

# Output lists
file_list = []
total_error_numbers = []
spelling_error_numbers = []
grammar_error_numbers = []
punctuation_error_numbers = []
syntax_error_numbers = []
style_error_numbers = []
other_error_numbers = []

# category dictionary
category_dict = {
    **dict.fromkeys([47, 1000, 34, 2, 45], "Spelling"),
    **dict.fromkeys([29, 5, 51, 21, 40, 105, 38, 37, 20, 43, 36, 19, 35, 18, 16], "Grammar"),
    **dict.fromkeys([46, 50, 42, 100], "Punctuation"),
    **dict.fromkeys([44, 15, 48, 13, 30, 31, 12, 23, 39], "Syntax"),
    **dict.fromkeys([102, 103, 104, 49], "Style"),
}

def main(): 
    # Read all .doc or .docx files in the target directory recursively and store the file names in a list 
    for root, dirs, files in os.walk(target_directory): 
        for file in files: 
            if file.endswith(".doc") or file.endswith(".docx"): 
                file_list.append(os.path.join(root, file)) 

    # print all the file names in the list
    for i in range(len(file_list)): 
        print(i, " ", file_list[i])

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
            docText = None
        # Length handler, no longer needed, decided to let too long documents go
        # while docText != None and len(docText) > 30000: 
        #     # take first 40000 characters
        #     tmp = docText[:30000]
        #     docText = docText[30000:]
        #     docTexts.append(tmp) 
        #     file_list.insert(i+1, file_list[i])
        docTexts.append(docText)

    if len(docTexts) == len(file_list): 
        print("Successfully read all files in the target directory.")

    # write to Ginger_Error_Details.csv file for error details
    with open('Single_Functions_by_Peicheng\Ginger_Error_Details.csv', 'w', newline='') as f: 
        writer = csv.writer(f)
        writer.writerow(['File Name', 'Sentence', 'Mistake Text', 'Error Message', 'replacements', 'Character/ Start Position in Text', 'Character/ End Position in Text', 'Error Type', 'Error Subtype'])

    # Send the HTTP POST request to the API endpoint for each file in the list
    for i in range(len(file_list)): 
        print("Processing file: ", file_list[i]) 
        total_error_number, spelling_error_number, grammar_error_number, punctuation_error_number, syntax_error_number, style_error_number, other_error_number = 0, 0, 0, 0, 0, 0, 0
        file_name = os.path.basename(file_list[i]) 
        if docTexts[i] == None: # Error reading file
            errString = "Error reading file"
            total_error_number, spelling_error_number, grammar_error_number, punctuation_error_number, syntax_error_number, style_error_number, other_error_number = errString, errString, errString, errString, errString, errString, errString
            total_error_numbers.append(total_error_number)
            spelling_error_numbers.append(spelling_error_number)
            grammar_error_numbers.append(grammar_error_number)
            punctuation_error_numbers.append(punctuation_error_number)
            syntax_error_numbers.append(syntax_error_number)
            style_error_numbers.append(style_error_number)
            other_error_numbers.append(other_error_number)

        response = requests.post(url, headers=headers, data=docTexts[i])
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
                    f.close()
                    
                # Extract the errors from the response
                if "GingerTheDocumentResult" in result:
                    documentResult = result["GingerTheDocumentResult"]
                    errors = documentResult["Corrections"] 
                    for error in errors: 
                        # print(error)
                        categoryId = int(error["TopCategoryId"])
                        # print(categoryId)
                        total_error_number += 1
                        supId = get_category(categoryId)
                        # print(supId)
                        if supId == "Spelling": 
                            spelling_error_number += 1
                        elif supId == "Grammar":
                            grammar_error_number += 1
                        elif supId == "Punctuation":
                            punctuation_error_number += 1
                        elif supId == "Syntax":
                            syntax_error_number += 1
                        elif supId == "Style":
                            style_error_number += 1
                        elif supId == "Other":
                            other_error_number += 1
                        # TODO: Finish this part
                        sentence = error["LrnFrg"] if "LrnFrg" in error else "N/A"
                        mistake_text = error["MistakeText"] if "MistakeText" in error else "N/A"
                        error_message = error["TopCategoryIdDescription"] if "TopCategoryIdDescription" in error else "N/A"
                        replacements = error["Suggestions"] if "Suggestions" in error else "N/A"
                        # print(replacements + " - " + len(replacements))
                        if replacements != "N/A" and len(replacements) > 0: 
                            replacements = replacements[0]
                            replacements = replacements["Text"] if "Text" in replacements else "N/A"
                        else:
                            replacements = "N/A"
                        start_position = error["From"] if "From" in error else "N/A"
                        end_position = error["To"] if "To" in error else "N/A"
                        error_type = supId
                        error_subtype = error["TopCategoryId"] if "TopCategoryId" in error else "N/A"
                        # Add to Ginger_Error_Details.csv file
                        add_to_csv(file_name, sentence, mistake_text, error_message, replacements, start_position, end_position, error_type, error_subtype)
                else:
                    print("No errors detected.")
            except json.decoder.JSONDecodeError as e:
                errString = "Failed to parse JSON response"
                print(f"Failed to parse JSON response: {e}")
                total_error_number, spelling_error_number, grammar_error_number, punctuation_error_number, syntax_error_number, style_error_number, other_error_number = errString, errString, errString, errString, errString, errString, errString
        else:
            print(f"Request failed with status code {response.status_code}.")
            errString = "Request failed with status code " + str(response.status_code) + ": " + str(response.text)
            total_error_number, spelling_error_number, grammar_error_number, punctuation_error_number, syntax_error_number, style_error_number, other_error_number = errString, errString, errString, errString, errString, errString, errString

        # append error numbers to the list
        total_error_numbers.append(total_error_number)
        spelling_error_numbers.append(spelling_error_number)
        grammar_error_numbers.append(grammar_error_number)
        punctuation_error_numbers.append(punctuation_error_number)
        syntax_error_numbers.append(syntax_error_number)
        style_error_numbers.append(style_error_number)
        other_error_numbers.append(other_error_number)

        print("Total error number\t Spelling error number\t Grammar error number\t Punctuation error number\t Syntax error number\t Style error number\t Other error number")
        print(total_error_number, "\t", spelling_error_number, "\t", grammar_error_number, "\t", punctuation_error_number, "\t", syntax_error_number, "\t", style_error_number, "\t", other_error_number)

    # write to csv file
    write_to_csv(file_list, total_error_numbers, spelling_error_numbers, grammar_error_numbers, punctuation_error_numbers, syntax_error_numbers, style_error_numbers, other_error_numbers)

    



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

def get_category(categoryId):
    return category_dict.get(categoryId, "Other")

def write_to_csv(file_list, total_error_numbers, spelling_error_numbers, grammar_error_numbers, punctuation_error_numbers, syntax_error_numbers, style_error_numbers, other_error_numbers):
    # Write to Ginger_Error_Stats.csv file
    with open('Single_Functions_by_Peicheng\Ginger_Error_Stats.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['File Name', 'Total Error Number', 'Spelling Error Number', 'Grammar Error Number', 'Punctuation Error Number', 'Syntax Error Number', 'Style Error Number', 'Other Error Number'])
        for i in range(len(file_list)):
            file_name = os.path.basename(file_list[i]) 
            writer.writerow([file_name, total_error_numbers[i], spelling_error_numbers[i], grammar_error_numbers[i], punctuation_error_numbers[i], syntax_error_numbers[i], style_error_numbers[i], other_error_numbers[i]])
        f.close()

def add_to_csv(file_name, sentence, mistake_text, error_message, replacements, start_position, end_position, error_type, error_subtype):
    # Add to Ginger_Error_Details.csv file
    with open('Single_Functions_by_Peicheng\Ginger_Error_Details.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        try: 
            writer.writerow([file_name, sentence, mistake_text, error_message, replacements, start_position, end_position, error_type, error_subtype])
        except UnicodeEncodeError as e:
            err = "UnicodeEncodeError: " + str(e)
            writer.writerow([file_name, err, err, err, err, err, err, err, err])
        f.close()
    

if __name__ == "__main__":
    main()