import os   
from extract_code import execute_extraction
import zipfile
import shutil

def delete_projects_in_unzip_folders():
    for item in os.listdir(projects_unzip):
        if item == '.gitkeep':
            continue
        
        item_path = os.path.join(projects_unzip, item)

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)

def copy_zip_file(source_zip_path, target_directory):

    if not os.path.isfile(source_zip_path):
        print(f"Error: ZIP file not found at '{source_zip_path}'")
        return

    os.makedirs(target_directory, exist_ok=True)

    zip_filename = os.path.basename(source_zip_path)
    target_path = os.path.join(target_directory, zip_filename)

    shutil.copy(source_zip_path, target_path)
    print(f"Copied '{source_zip_path}' to '{target_path}'")

def generate_project_list_and_copy_zips(source_directory, output_directory):
    try:
        repository_path = os.path.join(output_directory, "repository")
        os.makedirs(repository_path, exist_ok=True)

        project_entries = [
            os.path.join("repository", file_name)
            for file_name in os.listdir(source_directory)
        ]

        project_list_path = os.path.join(output_directory, "projects-list.txt")
        with open(project_list_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(project_entries))

        for file_name in os.listdir(source_directory):
            source_zip_path = os.path.join(source_directory, file_name)
            copy_zip_file(source_zip_path, repository_path)

        print(f"Project list saved to '{project_list_path}'")

    except Exception as error:
        print(f"An error occurred: {error}")


os.system('sudo chown -R denis:denis /home/denis/SourcererCC')
os.system('sudo chmod -R u+w /home/denis/SourcererCC')

os.system('cd tokenizers/block-level && sudo ./cleanup.sh')
os.system('cd clone-detector && sudo ./cleanup.sh')

generate_project_list_and_copy_zips('projects', 'tokenizers/block-level')

print("="*15 + "TOKENIZATION" + "="*15)
os.system('cd tokenizers/block-level && python3 tokenizer.py zipblocks')

source_file = 'tokenizers/block-level/blocks_tokens/files-tokens-0.tokens'
destination_dir = 'clone-detector/input/dataset'
os.makedirs(destination_dir, exist_ok=True)

# Define the destination file path with the new name
destination_path = os.path.join(destination_dir, 'blocks.file')

# Copy the file with the new name
shutil.copy(source_file, destination_path)

print("="*15 + "CLONE DETECTION" + "="*15)
os.system('cd clone-detector && python3 controller.py')

print("="*15 + "FORMMAT CLONES" + "="*15)
os.system('cat clone-detector/NODE_*/output8.0/query_* > results.pairs')

for folder in os.listdir('projects'):
    os.system(f'unzip -oq projects/{folder} -d projects_unzip')

source_folder = 'projects'
projects_unzip ='projects_unzip'
for filename in os.listdir(source_folder):
    if filename.lower().endswith('.zip'):
        zip_path = os.path.join(source_folder, filename)

        if zipfile.is_zipfile(zip_path):
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(projects_unzip)
            print(f"Descompactado: {zip_path} -> {projects_unzip}")

os.system('sudo rm -rf tokenizers/block-level/repository')

execute_extraction()

delete_projects_in_unzip_folders()

print("="*15 + "FINISH" + "="*15)