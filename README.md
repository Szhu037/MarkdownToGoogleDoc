
# Markdown to Google Docs Converter
This project provides a Python script that converts meeting notes written in Markdown format into a well-formatted Google Doc, using the Google Docs API. It preserves the structure of the original notes (headers, bullet points, checkboxes, etc.) and applies appropriate Google Docs styles.

## Description
The script converts meeting notes written in Markdown format into a Google Doc with the following formatting requirements:

Main title ("Product Team Sync") is converted to Heading 1.
Section headers ("Attendees", "Agenda", etc.) are converted to Heading 2.
Sub-section headers under "Agenda" are converted to Heading 3.
Bullet points and checkboxes are converted with proper indentation and formatting.
Assignee mentions (e.g., @name) are highlighted with bold styling.
Footer information such as "Meeting recorded by" and "Duration" is styled distinctly.
