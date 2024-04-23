import os
import sys
import time
import subprocess



if __name__ == "__main__":
    name = sys.argv[1]
    service = sys.argv[2]

    subprocess.run("cd services && python run_service.py all", shell=True)

    current_path = os.getcwd()
    time.sleep(300)

    if name == "evomaster":
        if service == "fdic":
            subprocess.run("tmux new -d -s evo1 'cd tool/evomaster/fdic && bash ./tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s evo2 'cd tool/evomaster/genome-nexus && bash ./tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s evo3 'cd tool/evomaster/language-tool && bash ./tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s evo4 'cd tool/evomaster/ocvn && bash ./tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s evo5 'cd tool/evomaster/ohsome && bash ./tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s evo6 'cd tool/evomaster/omdb && bash ./tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s evo7 'cd tool/evomaster/rest-countries && bash ./tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s evo8 'cd tool/evomaster/spotify && bash ./tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s evo9 'cd tool/evomaster/youtube && bash ./tool.sh'", shell=True)
    elif name == "resttestgen":
        if service == "fdic":
            subprocess.run("tmux new -d -s rtg1 'cd tool/resttestgen/fdic && bash ./tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s rtg2 'cd tool/resttestgen/genome-nexus && bash ./tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s rtg3 'cd tool/resttestgen/language-tool && bash ./tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s rtg4 'cd tool/resttestgen/ocvn && bash ./tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s rtg5 'cd tool/resttestgen/ohsome && bash ./tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s rtg6 'cd tool/resttestgen/omdb && bash ./tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s rtg7 'cd tool/resttestgen/rest-countries && bash ./tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s rtg8 'cd tool/resttestgen/spotify && bash ./tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s rtg9 'cd tool/resttestgen/youtube && bash ./tool.sh'", shell=True)
    elif name == "schemathesis":
        if service == "fdic":
            subprocess.run("tmux new -d -s schema1 'cd tool/schemathesis/fdic && bash ./tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s schema2 'cd tool/schemathesis/genome-nexus && bash ./tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s schema3 'cd tool/schemathesis/language-tool && bash ./tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s schema4 'cd tool/schemathesis/ocvn && bash ./tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s schema5 'cd tool/schemathesis/ohsome && bash ./tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s schema6 'cd tool/schemathesis/omdb && bash ./tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s schema7 'cd tool/schemathesis/rest-countries && bash ./tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s schema8 'cd tool/schemathesis/spotify && bash ./tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s schema9 'cd tool/schemathesis/youtube && bash ./tool.sh'", shell=True)
    elif name == "tcases":
        if service == "fdic":
            subprocess.run("tmux new -d -s tcases1 'cd tool/tcases/fdic && bash tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s tcases2 'cd tool/tcases/genome-nexus && bash tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s tcases3 'cd tool/tcases/language-tool && bash tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s tcases4 'cd tool/tcases/ocvn && bash tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s tcases5 'cd tool/tcases/ohsome && bash tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s tcases6 'cd tool/tcases/omdb && bash tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s tcases7 'cd tool/tcases/rest-countries && bash tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s tcases8 'cd tool/tcases/spotify && bash tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s tcases9 'cd tool/tcases/youtube && bash tool.sh'", shell=True)
    elif name == "arat-rl":
        if service == "fdic":
            subprocess.run("tmux new -d -s arat1 'cd tool/arat/fdic && bash tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s arat2 'cd tool/arat/genome-nexus && bash tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s arat3 'cd tool/arat/language-tool && bash tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s arat4 'cd tool/arat/ocvn && bash tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s arat5 'cd tool/arat/ohsome && bash tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s arat6 'cd tool/arat/omdb && bash tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s arat7 'cd tool/arat/rest-countries && bash tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s arat8 'cd tool/arat/spotify && bash tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s arat9 'cd tool/arat/youtube && bash tool.sh'", shell=True)
    elif name == "arat-nlp":
        if service == "fdic":
            subprocess.run("tmux new -d -s arat1 'cd tool/arat/fdic-nlp && bash tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s arat2 'cd tool/arat/genome-nexus-nlp && bash tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s arat3 'cd tool/arat/language-tool-nlp && bash tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s arat4 'cd tool/arat/ocvn-nlp && bash tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s arat5 'cd tool/arat/ohsome-nlp && bash tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s arat6 'cd tool/arat/omdb-nlp && bash tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s arat7 'cd tool/arat/rest-countries-nlp && bash tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s arat8 'cd tool/arat/spotify-nlp && bash tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s arat9 'cd tool/arat/youtube-nlp && bash tool.sh'", shell=True)
    elif name == "llamaresttest":
        if service == "fdic":
            subprocess.run("tmux new -d -s llama1 'cd tool/llama/fdic && bash tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s llama2 'cd tool/llama/genome-nexus && bash tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s llama3 'cd tool/llama/language-tool && bash tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s llama4 'cd tool/llama/ocvn && bash tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s llama5 'cd tool/llama/ohsome && bash tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s llama6 'cd tool/llama/omdb && bash tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s llama7 'cd tool/llama/rest-countries && bash tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s llama8 'cd tool/llama/spotify && bash tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s llama9 'cd tool/llama/youtube && bash tool.sh'", shell=True)
    elif name == "llamaresttest-ex":
        if service == "fdic":
            subprocess.run("tmux new -d -s llama1 'cd tool/llama2/fdic && bash tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s llama2 'cd tool/llama2/genome-nexus && bash tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s llama3 'cd tool/llama2/language-tool && bash tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s llama4 'cd tool/llama2/ocvn && bash tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s llama5 'cd tool/llama2/ohsome && bash tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s llama6 'cd tool/llama2/omdb && bash tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s llama7 'cd tool/llama2/rest-countries && bash tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s llama8 'cd tool/llama2/spotify && bash tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s llama9 'cd tool/llama2/youtube && bash tool.sh'", shell=True)
    elif name == "llamaresttest-ipd":
        if service == "fdic":
            subprocess.run("tmux new -d -s llama1 'cd tool/llama3/fdic && bash tool.sh'", shell=True)
        if service == "genome-nexus":
            subprocess.run("tmux new -d -s llama2 'cd tool/llama3/genome-nexus && bash tool.sh'", shell=True)
        if service == "language-tool":
            subprocess.run("tmux new -d -s llama3 'cd tool/llama3/language-tool && bash tool.sh'", shell=True)
        if service == "ocvn":
            subprocess.run("tmux new -d -s llama4 'cd tool/llama3/ocvn && bash tool.sh'", shell=True)
        if service == "ohsome":
            subprocess.run("tmux new -d -s llama5 'cd tool/llama3/ohsome && bash tool.sh'", shell=True)
        if service == "omdb":
            subprocess.run("tmux new -d -s llama6 'cd tool/llama3/omdb && bash tool.sh'", shell=True)
        if service == "rest-countries":
            subprocess.run("tmux new -d -s llama7 'cd tool/llama3/rest-countries && bash tool.sh'", shell=True)
        if service == "spotify":
            subprocess.run("tmux new -d -s llama8 'cd tool/llama3/spotify && bash tool.sh'", shell=True)
        if service == "youtube":
            subprocess.run("tmux new -d -s llama9 'cd tool/llama3/youtube && bash tool.sh'", shell=True)

    time.sleep(3600)
    subprocess.run("tmux kill-server", shell=True)