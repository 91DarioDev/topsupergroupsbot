# TopSupergroupsBot
A telegram bot for telegram public groups leaderboards


<img src="../master/resources/logo/trasparencylogo.png" width="300">

## How to install:

### On Linux:

- Move to the path where you want to create the virtualenv directory
```
cd path
```
- Create a folder containing the env named `tsbenv`
```
virtualenv -p python3 tsbenv 
```
- Install the bot from the zip
```
tsbenv/bin/pip install https://github.com/91dariodev/topsupergroupsbot/archive/master.zip
```
- Run the bot. The first parameter of the command is `the config.yaml` file. Copy from the source `config.example.yaml` and create a file named `config.yaml` replacing values.
```
tsbenv/bin/topsupergroupsbot path/config.yaml
```
- To upgrade the bot:
```
tsbenv/bin/pip install --upgrade https://github.com/91dariodev/topsupergroupsbot/archive/master.zip
```
- To delete everything:
```
cd ..
rm -rf tsbenv
```
