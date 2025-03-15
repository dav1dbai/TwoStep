# TwoStep: Multi-agent Task Planning using Classical Planners and Large Language Models
This repo contains the official source code of `TwoStep` for generating multi-agent plans based on problems decribed by natural language, in symbolic domains.

Check out our [paper](https://arxiv.org/abs/2403.17246) and [website](https://glamor-usc.github.io/twostep/)!

## Getting Started

1. Install required python libraries with ```pip install -r requirements.txt```
2. Install [fast-downward](https://drive.google.com/file/d/16HlP14IN06asIXYAZ8RHR1P7-cEYwhA6/view). For more details on fast-downward, please check the official [github repo](https://github.com/aibasel/downward) and the fast-downward [website](https://www.fast-downward.org/).
3. Create a .env file to store your OpenAI API key— alternatively any API key with an OpenAI compatible API. 


## Running an Experiment


To run an individual multi-agent planning experiment, use `helper_script_n_agents.py`:

```
python helper_script_n_agents.py --domain $DOMAIN --time-limit $LIMIT --task_id $ID --num_agents $N --run $RUN --model $MODEL
```

Parameters:
- `$DOMAIN`: One of the 5 domains: blocksworld, barman, grippers, termes, and tyreworld
- `$LIMIT`: Number of seconds allocated for fast-downward to spend on planning each subgoal/goal
- `$ID`: Task identifier (1-20) for each domain
- `$N`: Number of agents/subgoals to generate
- `$RUN`: Run identifier for tracking experiments
- `$MODEL`: LLM model to use (e.g., 'gpt-4o')

This script will:
1. Generate N subgoals using the specified LLM
2. Create a multi-agent plan where each agent handles a subgoal
3. Print out the final merged plan with metrics for execution time
4. Benchmark the multi-agent solution against a single agent execution of the same task

The system saves single agent results to the folder SA_cache, which we have provided, to save time by not replanning tasks that have already been solved.

## Running Multiple Experiments

To run a batch of experiments, you can use the `run_experiments.sh` script:

```
./run_experiments.sh --output-file results.txt --summary-file summary.txt --python-script helper_script_n_agents.py --num-agents N --model MODEL_NAME --run RUN_ID --time-limit SECONDS --domains DOMAIN1,DOMAIN2 --tasks ID1,ID2,ID3
```

Parameters:
- `--output-file`: File to store detailed experiment results
- `--summary-file`: File to store the summary of all experiments
- `--python-script`: Script to run (helper_script_n_agents.py for multi-agent planning)
- `--num-agents`: Number of agents to use
- `--model`: LLM model to use (e.g., 'gpt-4o')
- `--run`: Run identifier
- `--time-limit`: Time limit in seconds for each planning task
- `--domains`: Comma-separated list of domains to test
- `--tasks`: Comma-separated list of task IDs to run

Example:
```
./run_experiments.sh --output-file termes_results.txt --summary-file termes_summary.txt --python-script helper_script_n_agents.py --num-agents 4 --model 'gpt-4o' --run 1001 --time-limit 250 --domains termes --tasks 1,2,3,4,5
```

This simply iterates over all experiments and saves their results to a file, then calls `processor.py` and formats everything in the summary file. 

## Visualizing Results
`graph_results.py` contains the code we used to plot the graphs in our paper. We store a dictionary of all results that can be updated with your own results—— if you want to rerun the multi-agent planning, you can run 
```
python solve_pddl_MA.py --time-limit SECONDS --domain DOMAIN
```
Parameters
- `--time-limit`: Time limit in seconds for the planner.
- `--domain`: the domain to test

## Project Structure

```
TwoStep/
├── domains/                     # Domain definitions and problem files
│   ├── barman/                  # Single-agent barman domain
│   │   ├── domain.nl            # Natural language domain description
│   │   ├── description_generator.py  # Problem description generator
│   │   ├── p*.nl                # Problem descriptions in natural language
│   │   └── p_example.sol        # Example solution files
│   ├── barman-multi/            # Multi-agent variant of barman domain
│   ├── blocksworld/             # Single-agent blocksworld domain
│   ├── blocksworld-multi/       # Multi-agent variant of blocksworld domain
│   ├── grippers/                # Single-agent grippers domain
│   ├── grippers-multi/          # Multi-agent variant of grippers domain
│   ├── termes/                  # Single-agent termes domain
│   ├── termes-multi/            # Multi-agent variant of termes domain
│   ├── tyreworld/               # Single-agent tyreworld domain
│   └── tyreworld-multi/         # Multi-agent variant of tyreworld domain
├── modules/                     # Core functionality modules
│   ├── generator.py             # Generates subgoals and handles LLM integration
│   ├── planner.py               # Planning functionality and integration with fast-downward 
│   ├── utils.py                 # Utility functions and constants
│   └── __init__.py
├── SA_cache/                    # Cache of single-agent solutions to avoid replanning
├── helper_script_n_agents.py    # Main script for running individual multi-agent experiments
├── run_experiments.sh           # Shell script for batch running multiple experiments
├── solve_pddl_MA.py             # Script for multi-agent PDDL problem solving
├── processor.py                 # Processes experiment results for analysis
├── graph_results.py             # Creates visualizations comparing different approaches
└── requirements.txt             # Python dependencies
