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
        json_dict = json.loads(file_contents)
    except Exception as e:
        error_message = f"Invalid JSON format: {str(e)}"
        raise HTTPException(status_code=400, detail=error_message)
    
    
    if code not in ["weak", "moderate", "strong"]:
        raise HTTPException(status_code=400, detail="Invalid Code Name")
    
    api_version = "deidentification-in-v1"


    # Set Method
    METHOD_POLICY = set_method_by_code(code)
    print(METHOD_POLICY)
    
    
    # Apply Deidentification
    for doc in json_dict['document']:
        
        for sentence in doc['sentences']:
            form = sentence['form']
            
            for PNE in sentence['PNE']:
                begin = PNE['begin']
                end = PNE['end']
                label = PNE['label']
                print(label)
                method = METHOD_POLICY[label]
                
                if "new_form" in sentence.keys():
                    new_form = sentence['new_form']
                    sentence['new_form'] = Deidentification(new_form, begin, end, method).process()
                    
                else:
                    sentence['new_form'] = Deidentification(form, begin, end, method).process()


    # Count set, turn, char
    number_of_set = len(json_dict['document'])
    number_of_turn = 0
    number_of_char = 0

    for doc in json_dict['document']:
        number_of_turn += len(doc['sentences'])
        for sentence in doc['sentences']:
            number_of_char += len(sentence['form'])


    # Record deidentification_process
    deidentification_process = {}
    deidentification_process['api'] = api_version
    deidentification_process['policy_code'] = code
    deidentification_process['number_of_set'] = number_of_set
    deidentification_process['number_of_turn'] = number_of_turn
    deidentification_process['number_of_char'] = number_of_char

    json_dict['deidentification_process'] = deidentification_process


    # Record deidentification_policy
    deidentification_policy = []
    for key in METHOD_POLICY.keys():
        tmp = {}
        tmp['label'] = key
        tmp['method'] = METHOD_POLICY[key]
        deidentification_policy.append(tmp)
    json_dict['deidentification_policy'] = deidentification_policy


    # Re-order first depth keys
    new_order = list(json_dict.keys()) 
    new_order.remove('document')  
    new_order.append('document')  

    json_dict = {key: json_dict[key] for key in new_order}

    
    return json_dict