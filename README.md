# LlamaRestTest

## Set up the experiment

### Machine Specification

Our experiments were conducted on Google Cloud E2 machines, each with a 16-core CPU and 36 GB of RAM.

### Download LlamaREST-EX and LlamaREST-IPD

Download these two SLMs (Small Language Models) in the root project directory.
- Download LlamaREST-EX using this [link](https://gtvault-my.sharepoint.com/:u:/g/personal/mkim754_gatech_edu/ET13K-NrtcxIpgYY7Z-OF-YBJTTVWVcuw_RKaJX10CvHOA?e=aLWvgN).
- Download LlamaREST-IPD using this [link](https://gtvault-my.sharepoint.com/:u:/g/personal/mkim754_gatech_edu/EY1wcOxGga5EkbnvRrKJJ4YB5HpBdcGPS-mLad7-70iqkw?e=bP4CVU).

Also, you can simply run the script `LlamaREST_EX.py` and `LlamaREST_IPD.py` to generate the LLMs! We used A100 GPU to run those.

You can find the training dataset for Inter-Parameter Dependency in this [link](https://huggingface.co/datasets/random1234321/REST-IPD/blob/main/train.txt) and Examples in this [link](https://huggingface.co/datasets/random1234321/REST-EX).

These are the used hyperparameter values for the training:

#### bitsandbytes Parameters
- **Model Name**: `Llama-2-7b-chat-hf`
- **Use 4-bit Precision**: `True`
- **Compute Dtype for 4-bit Models**: `float16`
- **Quantization Type**: `nf4`
- **Use Nested Quantization**: `False`

#### QLoRA Parameters
- **LoRA Attention Dimension (r)**: `64`
- **Alpha Parameter for LoRA Scaling**: `16`
- **Dropout Probability for LoRA Layers**: `0.1`

#### TrainingArguments Parameters
- **Output Directory**: `./results`
- **Number of Training Epochs**: `5`
- **Enable fp16/bf16 Training**: `fp16=False`, `bf16=False`
- **Batch Size per GPU for Training**: `4`
- **Batch Size per GPU for Evaluation**: `4`
- **Number of Update Steps to Accumulate Gradients**: `1`
- **Maximum Gradient Normal (Gradient Clipping)**: `0.3`
- **Initial Learning Rate (AdamW Optimizer)**: `2e-4`
- **Weight Decay**: `0.001`
- **Optimizer to Use**: `paged_adamw_32bit`
- **Learning Rate Schedule**: `constant`
- **Ratio of Steps for Linear Warmup**: `0.03`
- **Group Sequences by Length for Efficient Batching**: `True`
- **Save Checkpoint Every X Update Steps**: `25`
- **Log Every X Update Steps**: `25`

After the training, we used `llama.cpp` to quantize the model:

```
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
python3 conver.py [model_path] --outfile [output_name.gguf]
./quantize --help
```

You will have many options for quantization. You can decide the option based on your computing power! We used Q6_K quantization method which requires around 5GB per SLM.

### Software Dependencies and Installation

If your OS is Ubuntu 20.04, you can simply run our setup script with `sh setup.sh` command in your terminal.

The following software is required for the experiment:
- Docker: To containerize applications.
- Common Utilities: Includes software-properties-common, unzip, wget, gcc, git, vim, libcurl4-nss-dev, tmux, and mitmproxy.
- Java Development Kit (JDK): Both OpenJDK 8 and OpenJDK 11, along with Maven and Gradle for Java project management.
- Python 3: With pip and venv for managing Python packages and virtual environments.
- Jacoco: For code coverage analysis. 
- Testing tools: [Schemathesis](https://github.com/schemathesis/schemathesis), [EvoMaster](https://github.com/EMResearch/EvoMaster), [ARAT-RL](https://github.com/codingsoo/ARAT-RL), [RestTestGen](https://github.com/SeUniVr/RestTestGen), and [Tcases](https://github.com/Cornutum/tcases).
- Services in our `services` directory.

## Run the experiment

### Collect Authentication Tokens

OMDB and Spotify need authentication to run them. OMDB requires $10 per month to get the unlimited token (https://www.patreon.com/join/omdb). Spotify token can be obtained by visiting https://developer.spotify.com/console/get-playlists/ and clicking "Get Token".
Please replace TOKEN_HERE string in `services/omdb.py` and `services/spotify.py` with the obtained tokens.

### Run tools and services

After installing all the required software, you can run the tools with this command:

```
python run.py [tool's name] [service's name]
```

This command will run the tool and all the services in our benchmark for an hour. Possible tool names are `arat-rl`, `arat-nlp` (ARAT-RL with NLP2REST), `evomaster`, `resttestgen`, `schemathesis`, `llamaresttest`, `llamaresttest-ipd` (without LlamaREST-EX), `llamaresttest-ex` (without LlamaREST-IPD), and `tcases`. Possible service names are `fdic`, `genome-nexus`, `language-tool`, `ocvn`, `ohsome`, `omdb`, `rest-countries`, `spotify`, `youtube`.


```

```

### Collect the results

To collect the results, use the following command:

```
sh clean.sh
python collect.py
```

This will gather the coverage and number of responses for status codes 2xx, 4xx, and 500. The results will be stored in the `res.csv` file.


### Result

We show the detailed coverage report in this [link](https://docs.google.com/spreadsheets/d/1tP4z3ckS9SJQkXWu3EmPilHDBGiWm1BAqDYBO6aF6RQ/edit?usp=sharing) for each of 10 run.