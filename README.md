---
brew install python@3.12
python3.12 -m venv agent-env
source agent-env/bin/activate

## Next steps
### Confirm Python version inside your venv:

bash
python --version
It should show Python 3.12.x.

### Upgrade pip/setuptools/wheel (this avoids a lot of install headaches):

bash
pip install --upgrade pip setuptools wheel
### Install your lab requirements (or just the packages you need):

bash
pip install agent-framework==1.0.0b251209 agent-framework-azure-ai==1.0.0b251209
### If your lab folder has a requirements.txt, use:

bash
pip install -r requirements.txt
### Sanity check:

bash
python -c "from agent_framework.azure import AzureAIAgentClient; print('Import OK')"
If that runs without error, you’re ready to go.

## Azure login
az login