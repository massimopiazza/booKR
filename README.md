# Book knowledge retention manual steps
# [TODO] implement NotebookLM API to automate this


1. Read and highlight book using Apple's _Books_
   - all highlights will be synced to iCloud
   - ```.sql``` file containing all _Books_ highlights can be locally retrieved from macOS at:
     - ```ANNOTATION_DB_PATTERN = "~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/AEAnnotation*.sqlite"```
     - ```LIBRARY_DB_PATTERN = "~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/BKLibrary*.sqlite"```
2. Run script to generate ```.md``` file with highlights (retains color coding)
3. Use some online service to convert original ```.epub``` of the book you read to a ```.pdf```, e.g. [freepdfconvert.com](https://www.freepdfconvert.com/epub-to-pdf)
   - [TODO] try to do this locally via scripting if easy using some library, and high quality enough
4. Upload to [NotebookLM](https://notebooklm.google.com):
   - ```.pdf``` of entire book
   - ```.md``` file of highlights
5. Generate via NotebookLM:
   - Podcast
   - Briefing doc
   - Timeline doc
   - [optional] Study guide
6. Export _briefing doc_ to ```.pdf``` and ```html```
   1. Once generation done, click on _briefing doc_ and extract ```.html``` section
      - look for it in correspondence of search result "briefing document" (righ-click > inspect element, ```Shift + Cmd + F```)
   2. Copy ```.html``` and paste it into new ```.md``` file created via VS Code (you can also preview the file via ```Shift + Cmd + V```)
   3. From the ```.md``` file tab in VS Code access _command palette_ via ```Shift + Cmd + P```
   4. Type "export" > select ```"Markdown PDF: Export"``` (note: requires installing [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf) on VS Code)
7. Repeat previous step for _timeline doc_
