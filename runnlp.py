import os
import sys
import time
import subprocess



if __name__ == "__main__":
    name = sys.argv[1]
    token = sys.argv[2]

    subprocess.run("cd services && python run_service.py all " + token, shell=True)

    current_path = os.getcwd()
    time.sleep(300)

    if name == "evomaster" or name == "1":
        subprocess.run("tmux new -d -s evo1 'cd tool/evomaster/fdic && bash ./tool-nlp.sh'", shell=True)
        subprocess.run("tmux new -d -s evo2 'cd tool/evomaster/genome-nexus && bash ./tool-nlp.sh'", shell=True)
        subprocess.run("tmux new -d -s evo3 'cd tool/evomaster/language-tool && bash ./tool-nlp.sh'", shell=True)
        subprocess.run("tmux new -d -s evo4 'cd tool/evomaster/ocvn && bash ./tool-nlp.sh'", shell=True)
        subprocess.run("tmux new -d -s evo5 'cd tool/evomaster/ohsome && bash ./tool-nlp.sh'", shell=True)
        subprocess.run("tmux new -d -s evo6 'cd tool/evomaster/omdb && bash ./tool-nlp.sh'", shell=True)
        subprocess.run("tmux new -d -s evo7 'cd tool/evomaster/rest-countries && bash ./tool-nlp.sh'", shell=True)
        subprocess.run("tmux new -d -s evo8 'cd tool/evomaster/spotify && bash ./tool-nlp.sh'", shell=True)
        subprocess.run("tmux new -d -s evo9 'cd tool/evomaster/youtube && bash ./tool-nlp.sh'", shell=True)
    elif name == "resttestgen" or name == "2":
        subprocess.run("tmux new -d -s rtg1 'cd tool/resttestgen/fdic-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg2 'cd tool/resttestgen/genome-nexus-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg3 'cd tool/resttestgen/language-tool-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg4 'cd tool/resttestgen/ocvn-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg5 'cd tool/resttestgen/ohsome-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg6 'cd tool/resttestgen/omdb-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg7 'cd tool/resttestgen/rest-countries-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg8 'cd tool/resttestgen/spotify-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg9 'cd tool/resttestgen/youtube-nlp && bash ./tool.sh'", shell=True)
    elif name == "schemathesis" or name == "3":
        subprocess.run("tmux new -d -s schema1 'cd tool/schemathesis/fdic-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema2 'cd tool/schemathesis/genome-nexus-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema3 'cd tool/schemathesis/language-tool-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema4 'cd tool/schemathesis/ocvn-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema5 'cd tool/schemathesis/ohsome-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema6 'cd tool/schemathesis/omdb-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema7 'cd tool/schemathesis/rest-countries-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema8 'cd tool/schemathesis/spotify-nlp && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema9 'cd tool/schemathesis/youtube-nlp && bash ./tool.sh'", shell=True)
    elif name == "tcases" or name == "4":
        subprocess.run("tmux new -d -s tcases1 'cd tool/tcases/fdic-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases2 'cd tool/tcases/genome-nexus-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases3 'cd tool/tcases/language-tool-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases4 'cd tool/tcases/ocvn-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases5 'cd tool/tcases/ohsome-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases6 'cd tool/tcases/omdb-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases7 'cd tool/tcases/rest-countries-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases8 'cd tool/tcases/spotify-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases9 'cd tool/tcases/youtube-nlp && bash tool.sh'", shell=True)
    elif name == "arat-rl" or name == "5":
        subprocess.run("tmux new -d -s arat1 'cd tool/arat/fdic-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat2 'cd tool/arat/genome-nexus-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat3 'cd tool/arat/language-tool-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat4 'cd tool/arat/ocvn-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat5 'cd tool/arat/ohsome-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat6 'cd tool/arat/omdb-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat7 'cd tool/arat/rest-countries-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat8 'cd tool/arat/spotify-nlp && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat9 'cd tool/arat/youtube-nlp && bash tool.sh'", shell=True)
    elif name == "arat-rl" or name == "6":
        subprocess.run("tmux new -d -s arat1 'cd tool/arat/fdic-gpt && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat2 'cd tool/arat/genome-nexus-gpt && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat3 'cd tool/arat/language-tool-gpt && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat4 'cd tool/arat/ocvn-gpt && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat5 'cd tool/arat/ohsome-gpt && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat6 'cd tool/arat/omdb-gpt && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat7 'cd tool/arat/rest-countries-gpt && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat8 'cd tool/arat/spotify-gpt && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat9 'cd tool/arat/youtube-gpt && bash tool.sh'", shell=True)

    time.sleep(3600)
    subprocess.run("tmux kill-server", shell=True)
    with open("services/spotify.py", "r") as file:
        content = file.read()
    # Replace the word and save the modified content
    content = content.replace(token, "TOKEN_HERE")

    with open("services/spotify.py", "w") as file:
        file.write(content)