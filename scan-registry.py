import os
import sys
import csv 
import math
import getopt
import dotenv
import gitlab
import logging
import progressbar

# methods
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

# variables
version = "0.8"
output_file = ""

# init
dotenv.load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(message)s')

# .env
# gitlab_token = os.getenv('GITLAB_TOKEN',"")
# gitlab_uri = os.getenv('GITLAB_URI',"")

# args
opts, args = getopt.getopt(sys.argv[1:],"hi:o:v",["ifile=","ofile=", "help", "version"])

for opt, arg in opts:
    if opt in ("-h", "--help"):
        print ('''
scan-registry <options>

Options:
    -h, --help - get help
    -o, --ofile - output CSV file
    -v, --version - output version and settings of the script 

You should have variables in .env file (in context directory) or in the environment:

GITLAB_URI=https://<host-of-gitlab-instans>
GITLAB_TOKEN=<gitlab-token>

(!) environment has priority

        ''')
        exit(0)
    if opt in ("-v", "--version"):
        logging.info('📦 registry-scanner %s', version)
        logging.info('🦊 GITLAB_URI: "%s"', os.getenv('GITLAB_URI',""))
        logging.info('🦊 GITLAB_TOKEN: "%s"', "***" if os.getenv('GITLAB_TOKEN',"") else "")
        exit(0)
    elif opt in ("-o", "--ofile"):
        output_file = arg
        logging.info('💾 Result will be saved as CSV to "%s" file', output_file)


gl = gitlab.Gitlab(os.getenv('GITLAB_URI',""), os.getenv('GITLAB_TOKEN',""))
gl.auth()
# gl.enable_debug()

projects = gl.projects.list(all=True)

progressbar.streams.wrap_stderr()


gitlab_total_size = 0
report = []

counter = len(projects)
logging.info('🔎 Start scan %d projects', counter)
logging.info('----------------------')

for p in projects:
    
    logging.info('🔦 Scan project "%s"', p.name)

    if p.archived:
        logging.info('⏩ Skip archived "%s"', p.name)
        continue

    repositories = p.repositories.list(all=True)
    if repositories:
        for r in repositories:  
            tags = r.tags.list(all=True)

            total_size = 0

            if tags:
                for t in progressbar.progressbar(tags):
                    tag = r.tags.get(id=t.name)
                    total_size = total_size + tag.total_size
                    gitlab_total_size = gitlab_total_size + tag.total_size
            

            report_data = [
                p.name,
                p.path_with_namespace,
                p.web_url,
                r.location,
                total_size,
                convert_size(total_size)
            ]

            report.append(report_data)
            logging.info('🗄 Project "%s" spent space for registry "%s"', p.name, convert_size(total_size))
    
    else:
        logging.info('⏩ Project "%s" has not registry.', p.name)
        continue

logging.info('🚢 Total "%s"', gitlab_total_size)
logging.info('🛳 Total "%s"', convert_size(gitlab_total_size))

if output_file:
    with open(output_file, 'w') as f:
        w = csv.writer(f)
        w.writerow([
            "name" , 
            "path_with_namespace", 
            "web_url", 
            "location", 
            "size", 
            "human_size"
            ])
        logging.info("🖨 Result was saved  to CSV file %s", output_file)
        w.writerows(report)


    
    

    
    