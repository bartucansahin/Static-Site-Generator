This project is meant for creating a recusive static site generator from a markdown text. 

Change the content directory depending on your purpose, the most outer layer .md file will be the home page. 
Any sub-directories in this file could be entered given "[a nested post here](/sub-dir)" snippet in the outer .md file. 

You can change the style or add photos from the static directory. 

When you execute main.sh a local server will pop-up and your .md files will translated to HTML. 

The markdown is only capable of handling these boundries for now:
* Paragraph
* Heading
* Code
* Quote
* Unordered and ordered lists 

and 

* Bold
* Italic
* Code
* Image
* Link


