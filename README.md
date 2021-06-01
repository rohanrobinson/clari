# Clari - Helping Everyone Learn, No Matter Where They're From
Clari provides a service for summarizing and translating class materials into a student's native language from English. Class materials can be preloaded into the service, or students can copy-paste any material of their choice into the summarization and translation engine.


# Installation Instructions
1. Clone the repository
2. `cd` into the root of the repository
2. `python3 -m venv ./venv` to create the virtual environment
3. `source ./venv/bin/activate` to activate the virtual environment
4. `pip3 install -r requirements.txt`
5. `flask run` to start the server

This will instantiate the server on the url: `http://127.0.0.1:5000/`, which serves the web app Clari. Although we make use of tools from the IBM Cloud Suite, our app provides an easy-to-use and customizable web interface to use Clari. 

# To add new classes/lectures
Depending on the initial settings of the class, Panopto either produces a downloadable text file for all the captions or provides a `html` version of it stored as a `.rtf` document. Thus, we wrote two custom cleaning scripts, depending on the type of transcript, to prepare them as inputs for Clari. They can be executed in the following manner:

*Note: You must have either the* `.txt` *or* `.rtf` *files in a folder titled with the class name (such as* `CS89`*) within* `/panopto_captions`
1. **If the captions are in** `.txt` **format**: run `python cleaning_scripts/downloaded_captions.py <folder name>`
2. **If the captions are in** `.rtf` **format**: run `python cleaning_scripts/scraped_captions.py <folder name>`

After doing this, Clari will provide those classes as options for the summarization and translation task.  
