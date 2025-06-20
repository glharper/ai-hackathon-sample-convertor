# ai-hackathon-sample-convertor
Hackathon python script that converts samples in a given repo subfolder from Python to JS

Example usage:
```
python converter.py
python converter.py --repo_url <sample_subfolder_url> --library <JS_library_name> --docs <api_ref_doc_url>
```

TODO: API ref doc method discovery does not find actual methods properly, convertor makes a guess at converted method names

Possible improvements:
- Should be able to go from Language A to Language B instead of strictly Python to JS (generic was Sophia's original intent)
- Add parameter for coding guidelines URL (from Azure SDK, by default)
- Add parameter for example target sample
