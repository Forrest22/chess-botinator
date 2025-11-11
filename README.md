# Chess Botinator

Chess Botinator is a chess bot built to destroy Will's chess bot. Built to integrate to UCI, mainly will be using [lichess-bot](https://github.com/lichess-bot-devs/lichess-bot)

<img src="https://static.wikia.nocookie.net/phineasandferb/images/f/f2/Heinz_presents_his_Deflate-inator.jpg/revision/latest?cb=20120203220917" width="500px" alt="The future is bright for Chess Botinator">

### Using and installing venv

I like using venv for python so here's some setup help.

`python -m pip install virtualenv`

To create the virutual environment

`python -m venv [DIRECTORY]`

usually I use `python -m venv venv`

#### Windows

In cmd.exe

`venv\Scripts\activate.bat`

In PowerShell

`venv\Scripts\Activate.ps1`

#### Linux and MacOS

`source myvenv/bin/activate`

### Run the Most Amazing Chess Botinator

After making your venv, install from requirements `pip install -r requirements.txt`

You can now run the engine with `python engine.py` but this will only show you the UCI interface. Doesn't feel like much does it? If you'd like to play versus the chess bot locally

#### Playing versus the Chess Botinator

In order to play locally or on lichess.org you will need to compile the bot locally first as an executable. The following describes how to do this:

1. Install python: `python -m pip install pyinstaller`

2. Compile to binary as simple as: `pyinstaller --onefile engine.py`. This creates a binary executable in the folder `dist/`. This means that if you make any changes to the engine you'll need to recompile to reflect those changes. Remember this location for later.

##### Playing using a local GUI

1. Install a GUI that supports UCI engines, for these purposes I will be using [BanksiaGUI](https://banksiagui.com/download/).
Note: I am using BanksiaGUI because it supports my cross platform development needs as I develop on both Windows and Linux based operating systems.
2. Run the GUI executable
3. Click the `Settings` button and select the `Engines` sidebar item.
4. Click the `+` button to bring the Add Engine menu and in the `Engine file:` field link to your executable. Example: `/path/to/chess-botinator/dist/engine` and click OK.
5. Start a new game with the `New game` button and select chess-botinator as your opponent.

##### ROADMAP: Running with lichess-bot on lichess.org

I love lichess-bot, its a great way for me to test my engine. Here I hope to record how to run the chess-botinator using UCI. In order to install you'll need to compile this engine into a binary and run it with lichess-bot.

Side note if I my sole goal was to run with lichess-bot:
I coincidentally discovered [this piece of documentation](https://github.com/lichess-bot-devs/lichess-bot/wiki/Create-a-homemade-engine) that guides on how to create a homemade engine, but I already built most of my engine and had fun implementing the multithreading and time considerations. I would enjoy trying to implement that in the future to see if there are any differences in time controls.
The drawback of implementing it this way is that it doesn't seem to me that you'd not be able to communicate via UCI and would have to be ported out somehow if they ever outgrow being an appendage of lichess-bot.

##### Install lichess-bot and play on lichess.org

Then install [lichess-bot using their install steps](https://github.com/lichess-bot-devs/lichess-bot?tab=readme-ov-file#steps)

Next go to the lichess-directory and update the `config.yml` in lichess-bot and update the following fields:

- TBD
- Also need to finish setting up lichess token correctly.
