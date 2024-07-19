import subprocess
import sys
import os

# Function to install a package using pip
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import pandas and install if not found
try:
    import pandas as pd
except ImportError:
    print("Pandas not found. Installing...")
    install("pandas")
    import pandas as pd

# Specify the file path
file_path = 'archive/zomato.csv'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    sys.exit(1)

# Load the CSV file
zomoto_data = pd.read_csv(file_path, encoding='ISO-8859-1')
print(zomoto_data.head(10))
