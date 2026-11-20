# Technical Manual Assistant

Searches hardware manuals and returns troubleshooting passages with page-level or source-level citations.

## Usage
```bash
pip install -r requirements.txt
python src/manual_assistant.py index sample_manuals --index-dir outputs/index
python src/manual_assistant.py ask outputs/index "What should I check when the status LED flashes?"
```

The tool retrieves documented procedures rather than inventing undocumented repair steps.
