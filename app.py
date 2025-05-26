import json
import ollama
from google_apis import create_service

def construct_sheet_service():
    client_file = '<client_secret.json>'  # Replace with the name of your Google API client secret file
    API_NAME = 'sheets'
    API_VERSION = 'v4'  
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = create_service(client_file, API_NAME, API_VERSION, SCOPES)
    return service

def add_sheet_entry(service, spreadsheet_id, first_name, last_name, email):
    range_ = '<sheet_name>!B:B'  # Replace <sheet_name> with the actual name of your sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,   
        range=range_
    ).execute() 
    values_in_column_b = result.get('values', [])
    last_row = len(values_in_column_b) + 1  # Find the next empty row in column B
    values = [first_name, last_name, email]
    body = {    
        # Prepare the data to be added
        'values': [values]
    }
    response = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,      
        # Append the data to the specified sheet
        range=f'<sheet_name>!B{last_row}:D{last_row}', # Replace <sheet_name> with the actual name of your sheet
        valueInputOption='RAW',
        body=body
    ).execute()

    return response
'''
    define the tool
    https://www.youtube.com/watch?v=J42vIcaoCSk&list=PLYnsS31F_VsCPENPT79e39uPdBfuyeF_h&index=4
    the video uses properties instead of parameters suggested here:
    https://medium.com/@danushidk507/ollama-tool-calling-8e399b2a17a8

    https://www.ibm.com/think/tutorials/local-tool-calling-ollama-granite
'''
# define ollama tool
def ollama_tools():
    return {
        'type': 'function',
        'function': {
            'description': 'Add a new entry to the Google Sheet',
            'parameters': {
                'type': 'object',
                'properties': {
                    'service': {
                        'type': 'object',  
                        'description': 'Google Sheets service object'
                    },
                    'spreadsheet_id': {
                        'type': 'string',   
                        'description': 'ID of the Google Sheet'
                    },
                    'first_name': {
                        'type': 'string',
                        'description': 'First name of the person'
                    },
                    'last_name': {
                        'type': 'string',
                        'description': 'Last name of the person'
                    },
                    'email': {
                        'type': 'string',
                        'description': 'email of the person'
                    }
                },           
                'required': ['service', 'spreadsheet_id', 'first_name', 'last_name', 'email']
            },            
        },
    }

def system_prompt():
    return """
    You are a data entry assistant; your job is to take user input and add it to Google Sheets and ensure that all required arguments are populated in the tool call.

    Required arguments for function 'add_sheet_entry' are:
    - service
    - spreadsheet_id
    - first_name
    - last_name
    - email
    
    If response is '{"entry_added": true}' reply only with "entry added" to the user, nothing else.

    Example of a correctly formatted tool call (dict):
    {
        'function': {
            'name': 'add_sheet_entry',
            'arguments': {
                'service': 'Google Sheets service object',
                'spreadsheet_id': '<google_sheet_id>',
                'first_name': 'John',   
                'last_name': 'Doe',
                'email': abc@gmail.com
            }
        }
    }
    """.strip()

def run():
    model = 'llama3.2'
    client = ollama.Client()    
    spreadsheet_id = 'your_google_sheet_id_here'  # Replace with your actual Google Sheet ID
    service = construct_sheet_service()

    messages = [
        {
            'role': 'system',
            'content': system_prompt()
        }        
    ]

    while True:
        prompt = input("Enter the first name, last name, and email (or 'exit' to quit): ")
        if prompt.lower() == 'exit':
            print("Exiting the program.")
            break
       
        messages.append({'role': 'user', 'content': prompt})  
        response = client.chat(
            model=model,
            messages=messages,
            tools=[ollama_tools()]    # tools description in string format      
        )   
        print(f"Response 1 from AI: {response.message}")

        if not response.message.tool_calls:
            print("No tool call in the response. it's response was: ")
            print(response.message.content)
            continue

        else:                   
            # Extract the function name and arguments
            available_funcitions = {
                'add_sheet_entry': add_sheet_entry, #point to the actual function
            }
            for tool in response.message.tool_calls:
                print("Tool call detected.", tool.function)
                    # Extract the function name and arguments
                function_to_call = available_funcitions.get(tool.function.name)
                print("Function to call:", function_to_call)
                print("Function arguments extract from the prompt:", tool.function.arguments)
                tool.function.arguments['service'] = service
                tool.function.arguments['spreadsheet_id'] = spreadsheet_id
                print("Function arguments after adding more args:", tool.function.arguments)
                # Call the function with the provided arguments
                function_response = function_to_call(**tool.function.arguments)   
                print("Function calling response:", json.dumps(function_response, indent=4))
                messages.append({
                    'role': 'tool',
                    'content': '{"Entry added": true}'
                })
                final_response = client.chat(
                    model=model,
                    messages=messages,
                    stream=False                    
                )   
                messages.append(final_response.message)
                print("Agent:", final_response.message.content)  
                print("\n")
                    
    
if __name__ == "__main__":
    run()