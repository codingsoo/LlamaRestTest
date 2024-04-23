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
        subprocess.run("tmux new -d -s evo1 'cd tool/evomaster/fdic && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s evo2 'cd tool/evomaster/genome-nexus && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s evo3 'cd tool/evomaster/language-tool && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s evo4 'cd tool/evomaster/ocvn && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s evo5 'cd tool/evomaster/ohsome && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s evo6 'cd tool/evomaster/omdb && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s evo7 'cd tool/evomaster/rest-countries && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s evo8 'cd tool/evomaster/spotify && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s evo9 'cd tool/evomaster/youtube && bash ./tool.sh'", shell=True)
    elif name == "resttestgen" or name == "2":
        subprocess.run("tmux new -d -s rtg1 'cd tool/resttestgen/fdic && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg2 'cd tool/resttestgen/genome-nexus && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg3 'cd tool/resttestgen/language-tool && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg4 'cd tool/resttestgen/ocvn && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg5 'cd tool/resttestgen/ohsome && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg6 'cd tool/resttestgen/omdb && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg7 'cd tool/resttestgen/rest-countries && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg8 'cd tool/resttestgen/spotify && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s rtg9 'cd tool/resttestgen/youtube && bash ./tool.sh'", shell=True)
    elif name == "schemathesis" or name == "3":
        subprocess.run("tmux new -d -s schema1 'cd tool/schemathesis/fdic && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema2 'cd tool/schemathesis/genome-nexus && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema3 'cd tool/schemathesis/language-tool && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema4 'cd tool/schemathesis/ocvn && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema5 'cd tool/schemathesis/ohsome && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema6 'cd tool/schemathesis/omdb && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema7 'cd tool/schemathesis/rest-countries && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema8 'cd tool/schemathesis/spotify && bash ./tool.sh'", shell=True)
        subprocess.run("tmux new -d -s schema9 'cd tool/schemathesis/youtube && bash ./tool.sh'", shell=True)
    elif name == "tcases" or name == "4":
        subprocess.run("tmux new -d -s tcases1 'cd tool/tcases/fdic && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases2 'cd tool/tcases/genome-nexus && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases3 'cd tool/tcases/language-tool && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases4 'cd tool/tcases/ocvn && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases5 'cd tool/tcases/ohsome && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases6 'cd tool/tcases/omdb && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases7 'cd tool/tcases/rest-countries && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases8 'cd tool/tcases/spotify && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s tcases9 'cd tool/tcases/youtube && bash tool.sh'", shell=True)
    elif name == "arat-rl" or name == "5":
        subprocess.run("tmux new -d -s arat1 'cd tool/arat/fdic && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat2 'cd tool/arat/genome-nexus && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat3 'cd tool/arat/language-tool && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat4 'cd tool/arat/ocvn && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat5 'cd tool/arat/ohsome && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat6 'cd tool/arat/omdb && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat7 'cd tool/arat/rest-countries && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat8 'cd tool/arat/spotify && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s arat9 'cd tool/arat/youtube && bash tool.sh'", shell=True)
    elif name == "resttestgpt" or name == "6":
        subprocess.run("tmux new -d -s gpt1 'cd tool/resttestgpt/fdic && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s gpt2 'cd tool/resttestgpt/genome-nexus && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s gpt3 'cd tool/resttestgpt/language-tool && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s gpt4 'cd tool/resttestgpt/ocvn && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s gpt5 'cd tool/resttestgpt/ohsome && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s gpt6 'cd tool/resttestgpt/omdb && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s gpt7 'cd tool/resttestgpt/rest-countries && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s gpt8 'cd tool/resttestgpt/spotify && bash tool.sh'", shell=True)
        subprocess.run("tmux new -d -s gpt9 'cd tool/resttestgpt/youtube && bash tool.sh'", shell=True)
    elif name == "llama" or name == "7":
        subprocess.run("tmux new -d -s llama1 'cd tool/llama/fdic && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama2 'cd tool/llama/genome-nexus && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama3 'cd tool/llama/language-tool && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama4 'cd tool/llama/ocvn && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama5 'cd tool/llama/ohsome && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama6 'cd tool/llama/omdb && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama7 'cd tool/llama/rest-countries && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama8 'cd tool/llama/spotify && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama9 'cd tool/llama/youtube && bash tool.sh'", shell=True)
    elif name == "llama2" or name == "8":
        subprocess.run("tmux new -d -s llama1 'cd tool/llama2/fdic && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama2 'cd tool/llama2/genome-nexus && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama3 'cd tool/llama2/language-tool && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama4 'cd tool/llama2/ocvn && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama5 'cd tool/llama2/ohsome && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama6 'cd tool/llama2/omdb && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama7 'cd tool/llama2/rest-countries && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama8 'cd tool/llama2/spotify && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama9 'cd tool/llama2/youtube && bash tool.sh'", shell=True)
    elif name == "llama3" or name == "9":
        subprocess.run("tmux new -d -s llama1 'cd tool/llama3/fdic && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama2 'cd tool/llama3/genome-nexus && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama3 'cd tool/llama3/language-tool && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama4 'cd tool/llama3/ocvn && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama5 'cd tool/llama3/ohsome && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama6 'cd tool/llama3/omdb && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama7 'cd tool/llama3/rest-countries && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama8 'cd tool/llama3/spotify && bash tool.sh'", shell=True)
        # subprocess.run("tmux new -d -s llama9 'cd tool/llama3/youtube && bash tool.sh'", shell=True)

    time.sleep(3600)
    subprocess.run("tmux kill-server", shell=True)
    with open("services/spotify.py", "r") as file:
        content = file.read()
    # Replace the word and save the modified content
    content = content.replace(token, "TOKEN_HERE")

    with open("services/spotify.py", "w") as file:
        file.write(content)