import json
from docx import Document

# Load the JSON file
with open('sample.postman_collection.json', 'r', encoding='utf-8') as f:
    api_data = json.load(f)

# Create a new Word document
doc = Document()


# Add a table with headers
table = doc.add_table(rows=1, cols=7)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Endpoint'
hdr_cells[1].text = 'Method'
hdr_cells[2].text = 'Request'
hdr_cells[3].text = 'Response'
hdr_cells[4].text = 'Description'
hdr_cells[5].text = 'Ready'
hdr_cells[6].text = 'Cycle'

# Process the items in the Postman collection
for item in api_data.get('item', []):
    request = item.get('request', {})
    responses = item.get('response', [])
    
    row_cells = table.add_row().cells
    # Endpoint
    row_cells[0].text = request.get('url', {}).get('raw', 'N/A').split('://')[-1].split('/', 1)[-1]
    
    # Method
    row_cells[1].text = request.get('method', 'N/A')
    
    # Request
    request_details = []
    if 'body' in request and request['body'].get('mode') == 'raw':
        request_details.append(f"Body: {request['body']['raw']}")
    elif responses:
        # Check response's originalRequest for body (as in login endpoint)
        original_request = responses[0].get('originalRequest', {})
        if 'body' in original_request and original_request['body'].get('mode') == 'raw':
            request_details.append(f"Body: {original_request['body']['raw']}")
    if 'auth' in request and request['auth'].get('type') == 'bearer':
        request_details.append("Auth: Bearer Token")
    row_cells[2].text = '; '.join(request_details) if request_details else 'None'
    
    # Response
    response_details = []
    for resp in responses:
        code = resp.get('code', 'N/A')
        body = resp.get('body', 'N/A')
        response_details.append(f"{code}: {body}")
    row_cells[3].text = '; '.join(response_details) if response_details else 'None'
    
    # Description
    row_cells[4].text = item.get('name', 'N/A')
    
    # Ready and Cycle
    row_cells[5].text = 'done'
    row_cells[6].text = '1'

# Save the document
doc.save('./out_api_documentation.docx')
