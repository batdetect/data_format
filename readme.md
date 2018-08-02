# Bat Audio File and Meta Data Standard
Here we propose formats for naming audio files and for storing their associated meta data. Suggestions are welcome!  

We also provide scripts for converting existing annotations to this format (see `demo_save/save_metadata.py`) and for loading annotations to view them (see `demo_read/read_annotations.py`). There is also an example meta data json file in `demo_read/demo_metadata.json`.  

So that species annotations are consistent across different data collectors we maintain a list of species called `taxa.json`.  


## File naming
To simplify the sharing of audio files we suggest the following naming format.  

`Year-Month-Day_Hour-Minute-Second_Lat_long_TimeExpansion_FileNumber.wav`

### Details

The individual fields represent the following:  

`Year` 4 digit number e.g 2018  
`Month` 2 digit number [01, ..., 12] e.g. 01 = January  
`Day` 2 digit number [01, ..., 31] e.g. 01 = 1st day of month

`Hour` 2 digit number 24 hrs [00, ..., 23] e.g. 00 = 12 am  
`Minute` 2 digit number [00, ..., 59]  
`Second` 2 digit number [00, ..., 59]  

`Lat` latitude in decimal degrees, up to a max of 5 decimal places [-90, ..., 90] e.g. 51.50735. Lower precision can be used if the location of the recording is sensitive. If the location is unknown, the values can bet set to `NA`.     
`Long` longitude in decimal degrees, up to a max of 5 decimal places [-180, ..., 180] e.g. -0.12776.  

`TimeExpansion` number specifying time expansion factor used during recording e.g. 1 means no time expansion, 10 indicates a factor of 10.  

`FileNumber` if multiple files are recorded at the same location, at the same time, this last entry can be used to differentiate them. By default this can be set to 0.    

### Examples
Correct examples:  
`2018-07-23_21-56-31_51.50735_-0.12776_1_0.wav`  
`2017-08-01_00-12-00_-27.56672_124.57031_10_0.wav`  
`2010-02-01_04-45-00_35.68_139.69_1_0.wav`  
`2010-02-01_04-45-00_NA_NA_10_0.wav`  - unknown recording location  

Incorrect examples:  
`2018-07-23_21-56-31_51.50735_-0.12776_1_0.WAV`  - .wav should be lower case  
`2009_02_01_11_31_31_12.407_-2.328_1_0.wav`  - date and time should be separated with `-` and not `_`  
`2009_2_1_21_11_31_12.407_-2.328_1_0.wav`  - there should be at least two digits for each entry in the date and time   


## Meta Data

Instead of trying to store all the relevant meta data in the filename e.g. the species name, the data collector etc., we instead define a structured meta data file to store all this additional information. One option would be to use a `.csv` file, but they can be problematic when there are additional fields added in the future, non-ascii characters, etc. Instead, we follow the annotation format of the [iNaturalist dataset](https://github.com/visipedia/inat_comp) and add additional fields specific to audio files. While this may seem slightly cumbersome, it will hopefully make sharing data much easier. The annotations are stored in [JSON format](http://www.json.org/).  

The annotations for a set of recordings can be stored in a single `.json` file as follows:  
```
{
  "audio_files" : [audio_file],
  "annotations" : [annotation]
}
```

#### Audio File Data
For the audio file we store the following fields:

```
audio_file{
  "id" : int,
  "file_name" : str,
  "sampling_rate" : int,
  "time_expansion_factor" : int,
  "duration" : float,
  "date_recorded" : datetime,
  "lat" : float,
  "long" : float,
  "license" : int,
  "rights_holder_name" : str,
  "notes" : str,
  "taxon" : int,
  "exhaustively_annotated" : bool
}
```

#### Annotation Data
For each audio file there can be an associated set of annotations where each annotation (`annotation`) contains a bounding box (`bbox`) specifying the [start_time, end_time, low_freq, high_freq] of an individual bat call. Time is recorded in seconds and frequency in kHz. We also keep track of the taxon (e.g. genus or species name if known), the ID of the individual bat so that calls from different individuals can be annotated in the same file, and the type of call. If only one species is present in a given audio file this can be noted in the `taxon` field in the `audio_file` data. If there are no bats present in the recording `taxon` can be set to `-1`. Alternatively, if the individual calls have been annotated (i.e. bounding boxes drawn around each call) this data can be stored in the `annotation` data.

```
annotation{
  "id" : int,
  "audio_file_id" : int,
  "bbox" : [float, float, float, float],
  "individual_id" : int,
  "taxon" : int,
  "date_created" : datetime,
  "annotator_name" : str,
  "call_type" : int
}
```

#### Additional Meta Data
To standardize data sharing we provide some additional data fields that can be indexed in the audio and annotation data.
This includes a standardized list of species in `taxa`. It may not be possible to annotate to species level, and so genus level can also be used. This field can also be set to `Bats`, taxon id 1, to indicate that the species is unknown. Calls can be annotated as either being one of: `echolocation`, `social`, `feeding`, or `unknown`.

It's up to the data owner to choose the license that is most suitable for their data. If you have no restrictions on your data and are happy for it to be used for any purpose provided you are credited we recommend the following license:  
[Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)  
Alternatively, if you don't want your data to be used for commercial purposes you could choose:  
[Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/)  

This information is stored in a single meta data file called `bat_metadata.json`.
```
{
  "info" : info,
  "taxa" : [taxon],
  "licenses" : [license],
  "call_types" : [call_type]
}
```

Where each of the arrays contain the following data:
```
taxon{
  "id" : int,
  "name" : str,
  "preferred_common_name" : str,
  "rank" : str
}

call_type{
  "id" : int,
  "name" : str
}

license{
  "id" : int,
  "name" : str,
  "url" : str
}
```

## Notes
All times e.g. file durations and call times in files should be in the un-time expanded time. Similarly, the sampling rate and the frequency annotations should be in the original un-time expanded time.    
