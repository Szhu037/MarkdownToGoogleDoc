
# Markdown to Google Docs Converter
This project provides a Python script that converts meeting notes written in Markdown format into a well-formatted Google Doc, using the Google Docs API. It preserves the structure of the original notes (headers, bullet points, checkboxes, etc.) and applies appropriate Google Docs styles.

## Description
The script converts meeting notes written in Markdown format into a Google Doc with the following formatting requirements:

1. Main title ("Product Team Sync") is converted to Heading 
2. Section headers ("Attendees", "Agenda", etc.) are converted to Heading
3. Sub-section headers under "Agenda" are converted to Heading
4. Bullet points and checkboxes are converted with proper indentation and formatting.
5. Assignee mentions (e.g., @name) are highlighted with bold styling.
6. Footer information such as "Meeting recorded by" and "Duration" is styled distinctly.
