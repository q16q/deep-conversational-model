# Deep Conversational Model
-"**maybe i'm going insane**"  
> [!NOTE]
> readme is being overwritten!!
## 💫 Requirements:
- python 3.10.11
- node.js
- [**cuda drivers**](https://developer.nvidia.com/cuda-downloads)
- [discord bot token](https://discord.com/developers)
## ⚡ Setup
```ps1
python -m venv ./.venv
./activate.ps1
pip install -r requirements.txt
cd ts
npm install
```
in .env file:
```ini
DISCORD_TOKEN=[token]
```
## 🪷 Usage
**dcm needs two consoles; first for server and second for discord.js bot**  
  
in first console:
```ps1
./activate.ps1
cd src
python nodebridge.py
```
in second:
```ps1
cd ts
npm start
```