# Python Cisco Video Endpoint Audit Tool

### Truth be told, there is nothing really "Cisco" about this.  It is really just comparing one JSON file to a "gold standard" JSON file.  

## Purpose

## How to run

This is a CLI application.  To run the application, after you've installed all the dependancies from the `requirements.txt` file, just run `python app.py`.

This will run all models that are under `Endpoint/` folder.  So if there is a `Endpoint/DX80` folder, it will run it against those endpoints in `Endpoint/DX80/InstallBase`.  

This does require a file structure for each endpoint folder to have a `Gold` folder as well with one "standard" JSON config file in it.  

## Caveats

Currently outputs to a JSON file in the `output` directory.  Should eventually upgrade this to include the model of the output. 