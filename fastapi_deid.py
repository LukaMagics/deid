# Opensource
from fastapi import FastAPI, Form, UploadFile, Request, HTTPException, File
from fastapi.responses import JSONResponse
import json

# Custom
from deidentification import Deidentification
from method import set_method_by_code


app = FastAPI()

@app.post("/deidentification-in-v1")
async def masking(file: UploadFile = File(...), code: str = Form(...)):
    # Exception
    try:
        file_contents = await file.read()
        json_data = json.loads(file_contents)
    except Exception as e:
        error_message = f"Invalid JSON format: {str(e)}"
        raise HTTPException(status_code=400, detail=error_message)
    
    
    if code not in ["all-masking", "weak", "moderate", "strong"]:
        raise HTTPException(status_code=400, detail="Invalid Code Name")
    

    docs = json_data
    api_version = "deidentification-in-v1"

    # Set Method
    METHOD_POLICY = set_method_by_code(code)
    
    
    # Apply Deidentification
    for doc in docs['document']:

        for sentence in doc['sentences']:
            form = sentence['form']

            for PNE in sentence['PNE']:
                begin = PNE['begin']
                end = PNE['end']
                label = PNE['label']
                method = METHOD_POLICY[label]

                if "new_form" in sentence.keys():
                    new_form = sentence['new_form']
                    sentence['new_form'] = Deidentification(new_form, begin, end, method).process()
                else:
                    sentence['new_form'] = Deidentification(form, begin, end, method).process()

                    
    # Re-order Json
    for doc in docs['document']:

        for i in range(len(doc['sentences'])):

            if 'new_form' in doc['sentences'][i].keys():
                sentence = doc['sentences'][i]
                new_order = ['form', 'new_form', 'pid', 'PNE']
                doc['sentences'][i] = {key: sentence[key] for key in new_order}


    # Record Process Info
    if 'process_info' in docs.keys():
        process_info = docs['process_info']
        process_info['deidentification_api'] = api_version
        process_info['deidentification_code'] = code
    else:
        tmp = {}
        tmp['deidentification_api'] = api_version
        tmp['deidentification_code'] = code
        docs['process_info'] = tmp

    
    return docs