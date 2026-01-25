# Week 1 — Linux Basics

This assignment focuses on fundamental Linux command-line operations.  
The objective is to become familiar with filesystem navigation, file manipulation, redirection, filtering, and basic dataset handling using terminal commands.

---

## Objectives

- Understand basic Linux directory structure
- Practice file and folder operations
- Learn input/output redirection
- Perform simple data inspection and filtering
- Gain confidence working in terminal-based workflows

---

## Environment

- Operating System: Linux (Ubuntu / WSL)
- Tools: Bash shell, core Linux utilities

---

## Tasks and Commands

### 1. Create folders and navigate directories
```bash
mkdir linux_basic
cd linux_basic
mkdir mlops
cd mlops
```

### 2. Download dataset
wget https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv

Alternative method: 

curl -O https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv

### 3. List configuration files
ls /etc/*.conf

### 4. Create and display text file
echo "Hello! MLOps Bootcamp has started." > mlops.txt
cat mlops.txt

### 5. Create files and write content
mkdir yellow
cd yellow

touch red.txt blue.txt

echo "My Name is Red" > red.txt
echo "My Name is Blue" > blue.txt

### 6. Append file contents
cat red.txt >> blue.txt
cat blue.txt >> red.txt

### 7. Copy files
cp red.txt ../red_copied.txt
cp blue.txt ../blue_copied.txt

### 8. Install and use tree command
sudo apt-get update
sudo apt-get install -y tree

Display directory structure:
tree yellow

### 9. Download another dataset
mkdir -p ~/datasets
wget -O ~/datasets/Wine.csv https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv

### 10. Inspect dataset
Display first 15 rows:
head -n 15 ~/datasets/Wine.csv

### 11. Filter dataset using awk
Filter rows where Alcohol content is greater than 14.0:
awk -F',' 'NR==1 || $1 > 14.0' ~/datasets/Wine.csv

---
### Summary
In this assignment, the following Linux concepts were practiced:

Directory and file management

File creation and content manipulation

Input/output redirection (>, >>)

Dataset downloading via terminal

Basic data inspection using head

Data filtering using awk

Understanding terminal-based data workflows

This week provided a strong foundation for working comfortably in Linux environments, which is essential for MLOps and production-grade systems.
---
#Author

** Tuğba Niksarlı **
MLOps & LLMOps Bootcamp — Week 1


