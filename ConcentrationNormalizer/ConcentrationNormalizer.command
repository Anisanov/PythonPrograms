# Alan Nisanov
# anisanov@berkeley.edu
# ConcentrationNormalizer.sh
# This script will download dependencies and execute the ConcentrationNormalizer script

# Installing Dependencies
pip3 install pandas
pip3 install -U scikit-learn
pip3 install openpyxl

# Opening Directory that has this script
ABSPATH="$(cd "$(dirname "$0")" && pwd)"
cd "$ABSPATH"

# Running python script
python3 ./ConcentrationNormalizer.py