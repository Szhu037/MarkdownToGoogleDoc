# Required Libraries
from google.colab import auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload
import markdown
import re

# Step 1: Google Docs Authentication
auth.authenticate_user()

# Initialize the Docs API client
docs_service = build('docs', 'v1')

# Step 2: Create a Google Doc
def create_google_doc(title):
    document = docs_service.documents().create().execute()
    doc_id = document['documentId']
    docs_service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {"insertText": {"location": {"index": 1}, "text": title}}
            ]
        }).execute()
    return doc_id

# Step 3: Format Markdown into Google Doc requests
def parse_markdown_to_google_doc(md_text):
    # Basic parsing of markdown into Google Docs Requests
    requests = []
    
    # Convert markdown to HTML first
    html = markdown.markdown(md_text)
    
    # Parsing headers and content
    def process_header(header_level, text):
        style = {1: 'HEADING_1', 2: 'HEADING_2', 3: 'HEADING_3'}
        requests.append({
            "insertText": {"location": {"index": 1}, "text": text + "\n"}
        })
        requests.append({
            "updateParagraphStyle": {
                "range": {"startIndex": 1, "endIndex": len(text)+1},
                "paragraphStyle": {"namedStyleType": style[header_level]},
                "fields": "namedStyleType"
            }
        })

    # Processing each markdown line (basic example for headers, bullet points)
    lines = md_text.split('\n')
    for line in lines:
        if line.startswith('# '):  # Heading 1
            process_header(1, line[2:])
        elif line.startswith('## '):  # Heading 2
            process_header(2, line[3:])
        elif line.startswith('### '):  # Heading 3
            process_header(3, line[4:])
        elif line.startswith('- '):  # Bullet points
            requests.append({
                "insertText": {"location": {"index": 1}, "text": line[2:] + "\n"}
            })
    
    return requests

# Step 4: Add action items and checkboxes
def add_action_items(doc_id, action_items):
    for item in action_items:
        checkbox = "☐"  # Unicode checkbox symbol
        assignee = re.search(r'@(\w+)', item)
        if assignee:
            item = item.replace(assignee.group(0), f"**{assignee.group(0)}**")  # Bold assignee
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={
                "requests": [
                    {"insertText": {"location": {"index": 1}, "text": f"{checkbox} {item}\n"}}
                ]
            }).execute()

# Step 5: Example Markdown Notes
markdown_notes = """
# Product Team Sync - May 15, 2023

## Attendees
- Sarah Chen (Product Lead)
- Mike Johnson (Engineering)
- Anna Smith (Design)
- David Park (QA)

## Agenda

### 1. Sprint Review
- Completed Features
  - User authentication flow
  - Dashboard redesign
  - Performance optimization
    - Reduced load time by 40%
    - Implemented caching solution
- Pending Items
  - Mobile responsive fixes
  - Beta testing feedback integration

### 2. Current Challenges
- Resource constraints in QA team
- Third-party API integration delays
- User feedback on new UI
  - Navigation confusion
  - Color contrast issues

### 3. Next Sprint Planning
- Priority Features
  - Payment gateway integration
  - User profile enhancement
  - Analytics dashboard
- Technical Debt
  - Code refactoring
  - Documentation updates

## Action Items
- [ ] @sarah: Finalize Q3 roadmap by Friday
- [ ] @mike: Schedule technical review for payment integration
- [ ] @anna: Share updated design system documentation
- [ ] @david: Prepare QA resource allocation proposal

## Next Steps
- Schedule individual team reviews
- Update sprint board
- Share meeting summary with stakeholders

## Notes
- Next sync scheduled for May 22, 2023
- Platform demo for stakeholders on May 25
- Remember to update JIRA tickets

---
Meeting recorded by: Sarah Chen
Duration: 45 minutes
"""

# Step 6: Create and populate Google Doc
doc_id = create_google_doc("Product Team Sync Notes")
requests = parse_markdown_to_google_doc(markdown_notes)

# Add Action Items and Update Doc
add_action_items(doc_id, ["@sarah: Finalize Q3 roadmap by Friday", 
                          "@mike: Schedule technical review for payment integration"])

# Update the document with requests
docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
