# USEFUL SHELL SCRIPTS FOR PHOTOGRAMMETRY  

**This folder collects basic shell scripts developed to ease the work in photogrammetry**  

### Compatibility:
- MacOS
- Linux
- Windows (WSL)
- Any OS that can run shell scripts (bash or zsh)

### Installation:  
1) Create a folder on your computer where you would like to store your callable scripts.  
2) Download and store the shell scripts in this folder.
3) Adapt your .bashrc or .zshrc file to make the created folder callable:
   - On Linux: `sudo gedit .bashrc` 
   - On MacOS: `sudo open .zshrc`  
4) Add the following line:  
   `export PATH="/path/to/my/callable/script_folder:$PATH"`  
   *(Change the path with the one of your script folder)*  
5) Check the shebang of your script(s)  
   —> `#!/bin/bash` if it is bash,  `#!/bin/zsh` if it is zsh  

### Usage:  
- Open a terminal  
- Run the script with the necessary arguments.  

---------
