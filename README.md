# Set up the experiment

## Machine Specification

Our experiments were conducted on Google Cloud E2 machines, each with a 16-core CPU and 36 GB of RAM.

## Software Dependencies and Installation

If your OS is Ubuntu 20.04, you can simply run our setup script with `sh setup.sh` command in your terminal.

The following software is required for the experiment:
- Docker: To containerize applications.
- Common Utilities: Includes software-properties-common, unzip, wget, gcc, git, vim, libcurl4-nss-dev, tmux, and mitmproxy.
- Java Development Kit (JDK): Both OpenJDK 8 and OpenJDK 11, along with Maven and Gradle for Java project management.
- Python 3: With pip and venv for managing Python packages and virtual environments.
- Jacoco: For code coverage analysis. 
- Testing tools: [Schemathesis](https://github.com/schemathesis/schemathesis), [EvoMaster](https://github.com/EMResearch/EvoMaster), [ARAT-RL](https://github.com/codingsoo/ARAT-RL), [RestTestGen](https://github.com/SeUniVr/RestTestGen), and [Tcases](https://github.com/Cornutum/tcases).
- Services in our `services` directory.

# Run the experiment

## Run tools and services

After installing all the required software, you can run the tools with this command:

```
python run.py [tool's name]
```

This command will run the tool and all the services in our benchmark for an hour. Possible tool names are `arat-rl`, `evomaster`, `resttestgen`, `schemathesis`, `llamaresttest`, and `tcases`. 

## Collect the results

To collect the results, use the following command:

```
sh clean.sh
python collect.py
```

This will gather the coverage and number of responses for status codes 2xx, 4xx, and 500. The results will be stored in the `res.csv` file.
