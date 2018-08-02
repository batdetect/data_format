# Creating Annotation File

It may be easier to store the audio meta data in a `.csv` file. To convert an existing file run `python save_metadata.py file_name.csv` where `file_name.csv` is the name of the file with the meta data e.g. `python save_metadata.py demo_audio_files.csv`.

Care should be taken to ensure that the headings are in the same format as `demo_audio_files.csv`. `file_name.csv` can have as many rows as there are audio files. `license` and `taxon` are integers specifying the corresponding ids. This does not convert individual call annotations. 