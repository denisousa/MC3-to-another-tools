# Documentation: https://docs.pmd-code.org/latest/pmd_userdocs_cpd.html

import json
import subprocess

def detect_clones_in_project(project_path, min_tokens=50, output_file="clones.json"):
    command = [
        "pmd.bat", "cpd",
        "--minimum-tokens", str(min_tokens),
        "--dir", project_path,
        "--language", "java",
        "--format", "text",
        "--ignore-comments"
    ]

    print(f"Running CPD on: {project_path}")
    print(f"Command: {' '.join(command)}")

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with open('./PMD/results/result-detect-clones-in-project.txt', 'w') as f:
        f.write(result.stdout.replace("\r\n", "\n"))

def detect_clones_between_projects(project1_path, project2_path, min_tokens=50):
    command = [
        "pmd.bat", "cpd",
        "--minimum-tokens", str(min_tokens),
        "--dir", project1_path,
        "--dir", project2_path,
        "--language", "java",
        "--format", "text",
    ]

    print(f"Running CPD between:\n - {project1_path}\n - {project2_path}")
    print(f"Command: {' '.join(command)}")

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    with open('./PMD/results/result-detect-clones-between-projects.txt', 'w') as f:
        f.write(result.stdout.replace("\r\n", "\n"))


project1 = "C:/Users/denis/Documents/projectsMySearch/MC3-to-another-tools/projects/eclipse.platform.swt"
project2 = "C:/Users/denis/Documents/projectsMySearch/MC3-to-another-tools/projects/eclipse.platform.ui"
    
detect_clones_in_project(project1)
detect_clones_between_projects(project1, project2)