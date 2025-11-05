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

You can now run the engine with `python engine.py`

#### Running with lichess-bot

I love lichess-bot, its a great way for me to test my engine. Here I hope to record how to run the chess-botinator using UCI.

<details>
<summary>Side note if I my sole goal was to run with lichess-bot</summary>

I coincidentally discovered [this piece of documentation](https://github.com/lichess-bot-devs/lichess-bot/wiki/Create-a-homemade-engine) that guides on how to create a homemade engine, but I already built most of my engine and had fun implementing the multithreading and time considerations. I would enjoy trying to implement that in the future to see if there are any differences in time controls.

The drawback of implementing it this way is that it doesn't seem to me that you'd not be able to communicate via UCI and would have to be ported out somehow if they ever outgrow being an appendage of lichess-bot.

</details>

In order to install you'll need to compile this engine into a binary and run it with lichess-bot.

##### Compile as an executeable

Install python: `python -m pip install pyinstaller`

Compile to binary as simple as: `pyinstaller --onefile .\engine.py`. This creates a binary executable in the folder `dist/`. For windows this will

##### Install and run with lichess-bot

Then install [lichess-bot using their install steps](https://github.com/lichess-bot-devs/lichess-bot?tab=readme-ov-file#steps)

Next go to the lichess-directory and update the `config.yml` in lichess-bot and update the following fields:

- TBD
- Also need to finish setting up lichess token correctly.
