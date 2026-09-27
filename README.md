# ai-engineering

### Create python virtual env using CMD
python --version
C:\Users\mohammad_tanvir\AppData\Local\Programs\Python
"C:\Users\mohammad_tanvir\AppData\Local\Programs\Python\Python313\python.exe"
uv venv --python "C:\Users\mohammad_tanvir\AppData\Local\Programs\Python\Python313\python.exe"
.venv\Scripts\activate

### Create python virtual env using WSL

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env 2>/dev/null || source $HOME/.cargo/env 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
uv --version
# Go to your project folder
cd /path/to/your/project
# Build the virtual environment folder (.venv)
uv venv
source .venv/bin/activate