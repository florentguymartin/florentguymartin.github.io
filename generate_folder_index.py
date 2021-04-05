"""
This module generates html indexes for folders recursively.

If my_dir is a folder in the root directory, running
$ python generate_folder_index --path my_dir
adds a file _index.html in my_dir and likewise recursively for all subfolders of my_dir.
The files _index.html contain a list with links to files and folder contained inside the given folder.
"""

import os
import logging
import click

logger = logging.getLogger()
logger.setLevel(logging.INFO)

EXTENSIONS = [
    '.html',
    '.pdf',
    '.tex',
]

INDEX_NAME = '_index.html'

def get_html_index(list_links: list, path: str):
    html_txt=f"""
<!DOCTYPE html>

<html lang="en">

<head>
	<!-- Required meta tags -->
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">

	<!-- Bootstrap CSS -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet"
		integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
	<link rel="stylesheet" href="css/style.css">

	<!-- Title -->
	<title></title>
</head>

<body>
	<div class="container">
    
		<div class="navtop">
			<header class="d-flex justify-content-center py-3">
				<ul class="nav nav-pills">
					<li class="nav-item"><a href="/index.html" class="nav-link">Home</a></li>
					<li class="nav-item"><a href="/research.html" class="nav-link">Research</a></li>
					<li class="nav-item"><a href="/teaching.html" class="nav-link active">Teaching</a></li>
				</ul>
			</header>
	</div>
        
    <div class="container">
    <h1>Content of the directory {path}</h1>
<ul>
"""
    link_items = list(list_links.items())
    link_items.sort(key= lambda x: x[0].lower())
    for link_display, link in link_items:
        html_txt += f"""        <li>
        <a href="{link}">{link_display}</a>
        </li>
        """
    html_txt += """
</ul>
</div>
</div>
</body>
</html>
"""
    
    return html_txt
    
def upper_case_first_letter(s: str):
    return s[0].upper() + s[1:] 

@click.command()
@click.option('--path', type=str, required=True)
def generate_indexes(path: str):
    """Generate recursively an index.html html document for each folder below path"""
    _generate_indexes(path=path)

def _generate_indexes(path: str):
    """Generate recursively an index.html html document for each folder below path"""
    logging.info(f"generate index for {path}")
    
    ls = os.listdir(path)
    if INDEX_NAME in ls:
        ls.remove(INDEX_NAME)
    logging.debug(f"all files in {path}: {ls}")
    
    files = [filename for filename in ls 
             if os.path.isfile(os.path.join(path, filename))]
    logging.debug(f"files in {path}: {files}")
    
    folders =[filename for filename in ls if os.path.isdir(os.path.join(path, filename))]
    
    logging.debug(f"folders in {path}: {folders}")
    folder_paths = [os.path.join(path, folder) for folder in folders]
    
    list_files_links = {
        upper_case_first_letter(file): file 
        for file in files if os.path.splitext(file)[1] in EXTENSIONS
    }
    logging.debug(f"list_files_links in {path}: {list_files_links}")
    
    list_folders_links = {
        upper_case_first_letter(folder): os.path.join(folder, INDEX_NAME) 
        for folder in folders
    }
    list_links = list_files_links.copy()
    list_links.update(list_folders_links)
    
    html_file = get_html_index(list_links=list_links, path=path)
    head, tail = os.path.split(path)
    index_file = os.path.join(path, INDEX_NAME)
    with open(index_file, "w") as f:
        f.write(html_file)
        f.close()
    
    for folder_path in folder_paths:
        _generate_indexes(path=folder_path)
    
    return None


if __name__ == '__main__':
    generate_indexes()