#!/bin/bash

# Function to print usage information
print_usage() {
  echo "Usage: $0 [options]"
  echo "Options:"
  echo "  --output-file FILE         Specify the output file (default: experiment_results.txt)"
  echo "  --summary-file FILE        Specify the summary file"
  echo "  --python-script FILE       Specify the Python script to run"
  echo "  --num-agents N1            Specify the number of agents"
  echo "  --run NUMBER               Specify the run number"
  echo "  --model MODEL              Specify the model to use"
  echo "  --domains DOMAIN1,DOMAIN2  Specify domains (comma-separated, default: grippers)"
  echo "  --tasks ID1,ID2,...        Specify task IDs (comma-separated, default: 1-20)"
  echo "  --time-limit LIMIT         Specify the time limit for each task (default: 60)"
  echo "  --help                     Display this help message"
}

# Default values
OUTPUT_FILE="experiment_results.txt"
PYTHON_SCRIPT=""
SUMMARY_FILE=""
# termes "tyreworld" "grippers" "barman" "blocksworld"
DOMAINS=("grippers" "termes" "tyreworld" "blocksworld" "barman")
TIME_LIMIT=60 # seconds
TASK_IDS=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20)
NUM_AGENTS=""
RUN=100
MODEL=""

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --output-file)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --summary-file)
            SUMMARY_FILE="$2"
            shift 2
            ;;
        --python-script)
            PYTHON_SCRIPT="$2"
            shift 2
            ;;
        --num-agents)
            NUM_AGENTS="$2"
            shift 2
            ;;
        --run)
            RUN="$2"
            shift 2
            ;;
        --model) 
            MODEL="$2"
            shift 2
            ;;
        --domains)
            IFS=',' read -ra DOMAINS <<< "$2"
            shift 2
            ;;
        --tasks)
            IFS=',' read -ra TASK_IDS <<< "$2"
            shift 2
            ;;
        --time-limit)
            TIME_LIMIT="$2"
            shift 2
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_usage
            exit 1
            ;;
    esac
done

# Function to run an experiment with given parameters
run_experiment() {
    local domain=$1
    local time_limit=$2
    local task_id=$3
    if [[ "$PYTHON_SCRIPT" == "helper_script_n_agents.py" ]]; then
      local num_agents=$4
      echo "Running experiment: Domain=$domain, Time Limit=$time_limit, Task ID=$task_id, Agents=$NUM_AGENTS"
      python "$PYTHON_SCRIPT" \
          --domain "$domain" \
          --time-limit "$time_limit" \
          --task_id "$task_id" \
          --run "$RUN" \
          --num_agents "$num_agents" \
          --model "$MODEL" \
          >> "$OUTPUT_FILE" 2>&1
    elif [[ "$PYTHON_SCRIPT" == "helper_script_until_n.py" ]]; then
      echo "Running experiment: Domain=$domain, Time Limit=$time_limit, Task ID=$task_id, Run=$RUN, Model=$MODEL"
      python "$PYTHON_SCRIPT" \
        --domain "$domain" \
        --time-limit "$time_limit" \
        --task_id "$task_id" \
        --run "$RUN" \
        --max_agents "6" \
        --model "$MODEL" \
        >> "$OUTPUT_FILE" 2>&1
    else
      echo "Running experiment: Domain=$domain, Time Limit=$time_limit, Task ID=$task_id"
      python "$PYTHON_SCRIPT" \
          --domain "$domain" \
          --time-limit "$time_limit" \
          --task_id "$task_id" \
          --run "$RUN" \
          --model "$MODEL" \
          >> "$OUTPUT_FILE" 2>&1
    fi
    echo "----------------------------------------" >> "$OUTPUT_FILE"
}

# Clear the output file if it exists
> "$OUTPUT_FILE"

# Iterate through various configurations
for domain in "${DOMAINS[@]}"; do
  for task_id in "${TASK_IDS[@]}"; do
    run_experiment "$domain" "$TIME_LIMIT" "$task_id" "$NUM_AGENTS"
  done
done

echo "All experiments completed. Results are in $OUTPUT_FILE"

python processor.py "$OUTPUT_FILE" "$SUMMARY_FILE"

echo "Summary file created: $SUMMARY_FILE"
