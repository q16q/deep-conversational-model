# Deep Conversational Model
-"**maybe i'm going insane**"  
> [!NOTE]
> readme is being overwritten!!
## requirements:
- python 3.10.11
- node.js
- everything in requirements.txt
- cuda drivers
- discord bot
## setup
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
## usage
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