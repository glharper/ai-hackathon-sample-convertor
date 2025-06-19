# ai-hackathon-sample-convertor
Hackathon python script that converts samples in a given repo subfolder from Python to JS

Example usage:
```
python converter.py
python converter.py --repo_url <sample_subfolder_url> --library <JS_library_name> --docs <api_ref_doc_url>
```

TODO: API ref doc method discovery does not find actual methods properly, convertor makes a guess at converted method names
