# Week 1 — Linux Basic Questions

This assignment covers fundamental Linux command-line operations including
directory management, file manipulation, redirection, filtering, and basic dataset handling.

---

## 1. Create a folder and change directory

```bash

mkdir linux_basic
cd linux_basic
mkdir mlops
cd mlops
wget https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv

# Alternative:
# curl -O https://raw.githubusercontent.com/erkansirin78/datasets/master/Churn_Modelling.csv

ls /etc/*.conf

echo "Hello! MLOps Bootcamp has started." > mlops.txt
cat mlops.txt

mkdir yellow
cd yellow

touch red.txt blue.txt

echo "My Name is Red" > red.txt
echo "My Name is Blue" > blue.txt

cat red.txt >> blue.txt
cat blue.txt >> red.txt

cp red.txt ../red_copied.txt
cp blue.txt ../blue_copied.txt

# Install tree (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y tree

tree yellow

mkdir -p ~/datasets
wget -O ~/datasets/Wine.csv https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv

# Print first 15 lines
head -n 15 ~/datasets/Wine.csv

# Filter rows where Alcohol > 14.0
awk -F',' 'NR==1 || $1 > 14.0' ~/datasets/Wine.csv
