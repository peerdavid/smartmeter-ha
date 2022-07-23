# Integration of Smartmeter(KaifaMA309) into HomeAssistant
This project integrates a KaifaMA309 smartmeter into HomeAssistant.

Before I start I wanna thank Micael Reitbauer through his great
blog post https://www.michaelreitbauer.at/kaifa-ma309-auslesen-smart-meter-evn/
and the shared source code
https://github.com/greenMikeEU/SmartMeterEVNKaifaMA309/
which made it quite easy to integrate the smartmeter into HomeAssistant.


# Setup

## Hardware
Please follow https://www.michaelreitbauer.at/kaifa-ma309-auslesen-smart-meter-evn/
I used exactly this hardware.

## Software
For the initial setup call `./setup.sh` which installs all the dependencies.
Then enter your key into the `smartmeter.key` file. This ensures
that you do not accidentally push your key to GitHub as it is gitignored.

# Run
Simply call `python main.py --key="YOUR_KEY"`. You can also add this to the bashrc file in order to
ensure that its running when your Raspberry restarts.