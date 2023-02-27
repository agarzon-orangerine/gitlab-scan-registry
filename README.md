# Gitlab Scanner Registry

The script helps you scan all non-archive registries for getting size of this registry.

You can save result to CSV table for your analytics  (see --help).

1. Install requirements (requirements.txt)
```
pip install -r requirements.txt
```
(!) Tip: Use `venv`.

2. Run script for getting help
```
python scan-registry.py --help
```
Help:
```
scan-registry <options>

Options:
    -h, --help - get help
    -o, --ofile - output CSV file
    -v, --version - output version and settings of the script 

You should have variables in .env file (in context directory) or in the environment:

GITLAB_URI=https://<host-of-gitlab-instans>
GITLAB_TOKEN=<gitlab-token>

(!) environment has priority
```

3. Example for starting of scanning
```
python scan-registry.py -o report.csv
```
Enjoy.