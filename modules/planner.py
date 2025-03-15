from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import os
import subprocess
import re
import time
import glob
import modules.utils as utils
import numpy as np
import sys

sys.setrecursionlimit(10000)

FAST_DOWNWARD_ALIAS = "lama"

AGENT_PREDICATES = {
    "barman": ['handempty', 'holding'],
    "barman-enabled": ['handempty', 'holding'],
    "blocksworld": ['arm-empty', 'holding'],
    "grippers": ['at-robby', 'free', 'carry'],
    "termes": ['has-block', 'at'],
    "tyreworld": [],
    "barman-multi": ['handempty', 'holding'],
    "blocksworld-multi": ['arm-empty', 'holding'],
    "termes-multi": ['has-block', 'at'],
    "tyreworld-multi": [],
    "tyreworld-enabled": [],
    "grippers-multi": ['at-robby', 'free', 'carry'],
}

def planner(expt_path, args_, subgoal_idx=-1):

    global args
    args = args_

    domain_pddl_file =  f'./domains/{args.domain}/domain.pddl'
    # if multiagent w single subgoal get subgoal pddl
    if subgoal_idx > 0:
        if subgoal_idx == args.num_agents:
            task_pddl_file_name =  f"./{expt_path}/p{args.task_id}_0.pddl"
            plan_file_name = f"./{expt_path}/p{args.task_id}_0_plan.pddl"
            info = 'multiagent main goal'
        else:
            task_pddl_file_name =  f"./{expt_path}/p{args.task_id}_{subgoal_idx}.pddl"
            plan_file_name = f"./{expt_path}/p{args.task_id}_{subgoal_idx}_plan.pddl"
            info = f'subgoal_{subgoal_idx}'
    # get default pddl > single agent
    else:
        task_pddl_file_name =  f"./domains/{args.domain}/p{args.task_id}.pddl"
        plan_file_name = f"./{expt_path}/p{args.task_id}_plan.pddl"
        info = 'singleagent'
    sas_file_name = plan_file_name + '.sas'
    output_path = plan_file_name + '.out'

    start_time = time.time()

    # run fastforward to plan
    os.system(f"python ./downward/fast-downward.py --alias {FAST_DOWNWARD_ALIAS} " + \
              f"--search-time-limit {args.time_limit} --plan-file {plan_file_name} " + \
              f"--sas-file {sas_file_name} " + \
              f"{domain_pddl_file} {task_pddl_file_name} > {output_path}")
    with open(output_path, "r") as f:
        output = f.read()
    
    if(output.find('Actual search time') == -1):
        print("planner broke")
        print(output)
        
    planner_search_time_1st_plan = float(output.split('Actual search time: ')[1].split('\n')[0].strip()[:-1])
    planner_total_time = float(output.split('Planner time: ')[1].split('\n')[0].strip()[:-1])
    planner_total_time_opt = float(output.split('Actual search time: ')[-1].split('\n')[0].strip()[:-1])
    first_plan_cost = int(output.split('Plan cost: ')[1].split('\n')[0].strip())
    #import ipdb; ipdb.set_trace()
    # collect the least cost plan
    best_cost = 1e10
    best_plan = None

    for fn in glob.glob(f"{plan_file_name}.*"):
        with open(fn, "r") as f:
            plans = f.readlines()
            cost = utils.get_cost(plans[-1])
            if cost < best_cost:
                best_cost = cost
                best_plan = "\n".join([p.strip() for p in plans[:-1]])

    end_time = time.time()
    if best_plan:
        print(f"[info][{info}][{args.domain}] task {args.task_id} takes {planner_total_time} sec, found a plan with cost {best_cost}")
        # print(planner_total_time, planner_total_time_opt, best_cost, planner_search_time_1st_plan, first_plan_cost)
        return planner_total_time, planner_total_time_opt, best_cost, planner_search_time_1st_plan, first_plan_cost
    else:
        print(f"[info][{info}][{args.domain}] task {args.task_id} takes {planner_total_time} sec, no solution found")
        return -1, -1, -1, -1, -1

def validator(expt_path, subgoal_idx=-1):
    print("validating")
    if subgoal_idx >= 0:
        output_path = f"./{expt_path}/p{args.task_id}_{subgoal_idx}_validation.txt"
    else:
        output_path = f"./{expt_path}/p{args.task_id}_validation.txt"
    output_file = open(output_path, "w")

    domain_pddl_file =  f'./domains/{args.domain}/domain.pddl'

    if subgoal_idx >= 0:
        task_pddl_file =  f"./{expt_path}/p{args.task_id}_{subgoal_idx}.pddl"
        # print("validating and getting plan for subgoal", subgoal_idx)
        plan_path = os.path.join(f"./{expt_path}", 
                                f"p{args.task_id}_{subgoal_idx}_plan.pddl" + '.*')
    else:
        task_pddl_file =  f"./{expt_path}/p{args.task_id}.pddl"
        plan_path = os.path.join(f"./{expt_path}", 
                                f"p{args.task_id}_plan.pddl" + '.*')

    best_cost = 10e6
    plan_file = ''
    for fn in glob.glob(plan_path):
        with open(fn, "r") as f:
            plans = f.readlines()
            cost = utils.get_cost(plans[-1])
            if cost < best_cost:
                best_cost = cost
                plan_file = fn
    # print("plan_file", plan_file)
    v_start = time.time()
    result = subprocess.run(["./downward/validate", "-v", domain_pddl_file, task_pddl_file, plan_file], stdout=subprocess.PIPE)
    v_end = time.time()
    #print("validated")
    output = result.stdout.decode('utf-8')
    output_file.write(output)
    if "Plan valid" in result.stdout.decode('utf-8'):
        return True, v_end - v_start
    else:
        return False, v_end - v_start

def get_updated_init_conditions(expt_path, validation_filename=None, pddl_problem_filename=None, pddl_problem_filename_edited=None, env_conds_only=True, is_main=False):
    # print("getting updated init conditions")
    # print("validation file", validation_filename)
    # validation_filename = f"./{expt_path}/p{args.task_id}_subgoal_validation.txt" if validation_filename==None else validation_filename
    with open(validation_filename, 'r') as f:
        validation = f.readlines()
    # print(pddl_problem_filename)
    # pddl_problem_filename_ =  f"./domains/{args.domain}/p{args.task_id}.pddl" if pddl_problem_filename==None else pddl_problem_filename
    with open(pddl_problem_filename, 'r') as f:
        pddl_problem = f.read()
    pddl_problem = pddl_problem.split('(:init')
    pddl_problem[1:] = pddl_problem[1].split('(:goal')
    pddl_problem[1] = pddl_problem[1].strip()[:-1] # remove last ')'
    init_conditions  = [cond.strip() for cond in pddl_problem[1].split('\n') if len(cond)>1]
    new_init_conditions = init_conditions.copy()
    for line in validation:
        if any([x in line for x in AGENT_PREDICATES[args.domain]]) and env_conds_only: # skip agent states
            continue
        if 'Adding' in line:
            added_condition = line.split('Adding')[1].strip()
            if added_condition not in new_init_conditions:
                new_init_conditions.append(added_condition)
        if 'Deleting' in line:
            deleted_condition = line.split('Deleting')[1].strip()
            if deleted_condition in new_init_conditions:
                new_init_conditions.remove(deleted_condition)

    pddl_problem[1] = list(new_init_conditions)
    # get new goal for next state, from subgoal we are passing new conditions into
    if is_main: # get original goal from domain descriptor
        with open(f"./domains/{args.domain}/p{args.task_id}.pddl", 'r') as f:
            next_pddl_problem = f.read() 
    else:
        with open(pddl_problem_filename_edited, 'r') as f:
            next_pddl_problem = f.read()
    next_pddl_problem = next_pddl_problem.split('(:init')
    next_pddl_problem[1:] = next_pddl_problem[1].split('(:goal')
    next_pddl_problem[1] = next_pddl_problem[1].strip()[:-1]
    
    pddl_problem = pddl_problem[0] + '(:init\n' + '\n'.join(pddl_problem[1]) + '\n)\n(:goal' + next_pddl_problem[2]

    # print("writing new edited pddl to", pddl_problem_filename_edited)
    with open(pddl_problem_filename_edited, 'w') as f:
        f.write(pddl_problem)

def get_updated_init_conditions_recurse(expt_path, validation_filename=None, pddl_problem_filename=None, pddl_problem_filename_edited=None, env_conds_only=True):
    validation_filename = f"./{expt_path}/p{args.task_id}_subgoal_validation.txt" if validation_filename==None else validation_filename
    with open(validation_filename, 'r') as f:
        validation = f.readlines()
    
    pddl_problem_filename_ =  f"./domains/{args.domain}/p{args.task_id}.pddl" if pddl_problem_filename==None else pddl_problem_filename
    with open(pddl_problem_filename_, 'r') as f:
        pddl_problem = f.read()
    pddl_problem = pddl_problem.split('(:init')
    pddl_problem[1:] = pddl_problem[1].split('(:goal')

    pddl_problem[1] = pddl_problem[1].strip()[:-1] # remove last ')'
    init_conditions  = set([cond.strip() for cond in pddl_problem[1].split('\n') if len(cond)>1])
    new_init_conditions = init_conditions
    for line in validation:
        if any([x in line for x in AGENT_PREDICATES[args.domain]]) and env_conds_only: # skip agent states
            continue
        added_conditions = set([line.split('Adding')[1].strip()]) if 'Adding' in line else set()
        deleted_conditions = set([line.split('Deleting')[1].strip()]) if 'Deleting' in line else set()
        new_init_conditions  = (new_init_conditions | added_conditions) - deleted_conditions

    pddl_problem[1] = list(new_init_conditions)
    pddl_problem = pddl_problem[0] + '(:init\n' + '\n'.join(pddl_problem[1]) + '\n)\n(:goal' + pddl_problem[2]

    pddl_problem_filename = pddl_problem_filename if pddl_problem_filename_edited==None else pddl_problem_filename_edited
    pddl_problem_filename_ =  f"./{expt_path}/p{args.task_id}_edited_init.pddl" if pddl_problem_filename==None else pddl_problem_filename
    with open(pddl_problem_filename_, 'w') as f:
        f.write(pddl_problem)


def validator_simulation_recursive(expt_path, logfile, multi=False):
    domain_pddl_file = f'./domains/{args.domain}/domain.pddl'
    task_pddl_file = f'./domains/{args.domain}/p{args.task_id}.pddl'
    with open(task_pddl_file, 'r') as f:
        task = f.read()

    agent_plans = []
    for i in range(args.num_agents):
        plan_path = os.path.join(f"./{expt_path}", f"p{args.task_id}_{i}_plan.pddl" + '.*')
        best_cost = float('inf')
        best_plan_file = None
        for fn in glob.glob(plan_path):
            with open(fn, "r") as f:
                plans = f.readlines()
                cost = utils.get_cost(plans[-1])
                if cost < best_cost:
                    best_cost = cost
                    best_plan_file = fn
        if best_plan_file:
            with open(best_plan_file, 'r') as f:
                agent_plans.append(tuple(f.readlines()[:-1]))  # Convert to tuple
        else:
            return float('inf'), False

    print(f"TASK: {args.domain} - {args.run} - {args.task_id}")

    global log_file
    log_file = logfile

    with open(log_file, 'a+') as f:
        f.write(f"TASK: {args.domain} - {args.run} - {args.task_id}\n")

    global execution_state
    execution_state = np.full([len(plan) + 1 for plan in agent_plans] + [args.num_agents + 1], float('inf'))

    plan_length = validator_sim_recursion_function(expt_path, domain_pddl_file, tuple([0] * args.num_agents), tuple(agent_plans), tuple([task] * args.num_agents))

    success = plan_length < float('inf')
    print(plan_length, success)
    if success:
        print("tracing optimal path")
        trace_optimal_path(execution_state, agent_plans, log_file)
    return plan_length, success

@lru_cache(maxsize=None)
def validator_sim_recursion_function(expt_path,domain_pddl_file, indices, agent_plans, agent_tasks, agent_to_execute=None):
    num_agents = len(agent_plans)
    
    if all(indices[i] == len(agent_plans[i]) for i in range(num_agents)):
        return 0

    state_index = indices + (agent_to_execute if agent_to_execute is not None else num_agents,)
    if execution_state[state_index] != float('inf'):
        return execution_state[state_index]

    if agent_to_execute is not None:
        result = execute_agent_action(expt_path, domain_pddl_file, indices, agent_plans, agent_tasks, agent_to_execute)
    else:
        plans = []
        for i in range(num_agents):
            if indices[i] < len(agent_plans[i]):
                plans.append(validator_sim_recursion_function(expt_path, domain_pddl_file, indices, agent_plans, agent_tasks, i))
        
        plans.append(execute_all_agents_action(expt_path, domain_pddl_file, indices, agent_plans, agent_tasks))

        result = 1 + min(plans)

    execution_state[state_index] = result
    return result

def execute_agent_action(expt_path, domain_pddl_file, indices, agent_plans, task_states, agent_index):
    val_path = f"./{expt_path}/agent{agent_index}_val_temp.txt"
    plan_path = f"./{expt_path}/agent{agent_index}_plan_temp.txt"
    task_paths = [f"./{expt_path}/agent{i}_task_temp.txt" for i in range(len(agent_plans))]

    with open(plan_path, 'w') as f:
        f.write(agent_plans[agent_index][indices[agent_index]])
    for i, task in enumerate(task_states):
        with open(task_paths[i], 'w') as f:
            f.write(task)

    output = subprocess.run(["./downward/validate", "-v", domain_pddl_file, task_paths[agent_index], plan_path], capture_output=True, text=True)
    with open(val_path, 'w') as f:
        f.write(output.stdout)

    if 'unsatisfied precondition' not in output.stdout:
        with open(log_file, 'a+') as f:
            f.write(f"Agent {agent_index}, {indices[agent_index]}, {agent_plans[agent_index][indices[agent_index]][:-1]}\n")

        new_task_states = list(task_states).copy()
        for i in range(len(agent_plans)):
            new_task_path = f"./{expt_path}/agent{i}_new_task_temp.txt"
            get_updated_init_conditions_recurse(expt_path, validation_filename=val_path, pddl_problem_filename=task_paths[i], pddl_problem_filename_edited=new_task_path, env_conds_only=(i != agent_index))
            with open(new_task_path, 'r') as f:
                new_task_states[i] = f.read()

        new_indices = list(indices)
        new_indices[agent_index] += 1
        return validator_sim_recursion_function(expt_path, domain_pddl_file, tuple(new_indices), agent_plans, tuple(new_task_states))
    else:
        return float('inf')

def execute_all_agents_action(expt_path, domain_pddl_file, indices, agent_plans, task_states):
    val_paths = [f"./{expt_path}/agent{i}_val_temp.txt" for i in range(len(agent_plans))]
    plan_paths = [f"./{expt_path}/agent{i}_plan_temp.txt" for i in range(len(agent_plans))]
    task_paths = [f"./{expt_path}/agent{i}_task_temp.txt" for i in range(len(agent_plans))]
    new_task_paths = [f"./{expt_path}/agent{i}_new_task_temp.txt" for i in range(len(agent_plans))]

    all_valid = True
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(len(agent_plans)):
            if indices[i] < len(agent_plans[i]):
                with open(plan_paths[i], 'w') as f:
                    f.write(agent_plans[i][indices[i]])
                with open(task_paths[i], 'w') as f:
                    f.write(task_states[i])
                
                futures.append(executor.submit(subprocess.run, ["./downward/validate", "-v", domain_pddl_file, task_paths[i], plan_paths[i]], capture_output=True, text=True))

        for i, future in enumerate(futures):
            output = future.result()
            with open(val_paths[i], 'w') as f:
                f.write(output.stdout)
            
            if 'unsatisfied precondition' in output.stdout:
                all_valid = False
                break
            get_updated_init_conditions_recurse(expt_path, validation_filename=val_paths[i], pddl_problem_filename=task_paths[i], pddl_problem_filename_edited=new_task_paths[i], env_conds_only=False)
            for j in range(len(agent_plans)):
                if i != j:
                    get_updated_init_conditions_recurse(expt_path, validation_filename=val_paths[i], pddl_problem_filename=task_paths[j], pddl_problem_filename_edited=new_task_paths[j], env_conds_only=True)

    if all_valid:
        with open(log_file, 'a+') as f:
            for i in range(len(agent_plans)):
                if indices[i] < len(agent_plans[i]):
                    f.write(f"Agent {i}, {indices[i]}, {agent_plans[i][indices[i]][:-1]}\n")

        for i in range(len(agent_plans)):
            if indices[i] < len(agent_plans[i]):
                get_updated_init_conditions_recurse(
                    expt_path, 
                    validation_filename=val_paths[i], 
                    pddl_problem_filename=task_paths[i], 
                    pddl_problem_filename_edited=new_task_paths[i], 
                    env_conds_only=False
                )
                for j in range(len(agent_plans)):
                    if i != j:
                        get_updated_init_conditions_recurse(
                            expt_path, 
                            validation_filename=val_paths[i], 
                            pddl_problem_filename=task_paths[j], 
                            pddl_problem_filename_edited=new_task_paths[j], 
                            env_conds_only=True
                        )

        new_indices = tuple(idx + 1 if idx < len(plan) else idx for idx, plan in zip(indices, agent_plans))
        new_task_states = []
        for path in new_task_paths:
            with open(path, 'r') as f:
                new_task_states.append(f.read())

        return validator_sim_recursion_function(expt_path, domain_pddl_file, new_indices, agent_plans, tuple(new_task_states))
    else:
        return float('inf')
    
def trace_optimal_path(execution_state, agent_plans, log_file):
    # Start at goal state
    indices = [len(plan) for plan in agent_plans]
    num_agents = len(agent_plans)
    path = []
    
    while any(idx > 0 for idx in indices):
        current_state = tuple(indices) + (num_agents,)
        
        # Try parallel first
        prev_indices = [idx - 1 if idx > 0 else 0 for idx in indices]
        prev_state = tuple(prev_indices) + (num_agents,)
        
        if prev_state in execution_state and execution_state[prev_state] != float('inf'):
            # Record which agents actually moved
            active_agents = []
            for i in range(num_agents):
                if indices[i] > prev_indices[i]:
                    active_agents.append((i, agent_plans[i][prev_indices[i]]))
            
            if len(active_agents) > 1:
                path.append(('parallel', active_agents))
                indices = prev_indices
                continue
        
        # If parallel didn't work, try single agent
        for agent in range(num_agents):
            if indices[agent] > 0:
                test_indices = list(indices)
                test_indices[agent] -= 1
                prev_state = tuple(test_indices) + (agent,)
                
                if prev_state in execution_state and execution_state[prev_state] != float('inf'):
                    path.append(('single', agent, agent_plans[agent][test_indices[agent]]))
                    indices = test_indices
                    break
    
    # Write the path in forward order
    with open(log_file, 'a+') as f:
        f.write("\nOptimal Plan Trace:\n")
        f.write("-" * 50 + "\n")
        
        for action in reversed(path):
            if action[0] == 'parallel':
                f.write("Parallel Execution:\n")
                for agent, plan_step in action[1]:
                    f.write(f"  Agent {agent}: {plan_step}")
                f.write("\n")
            else:
                f.write(f"Agent {action[1]}: {action[2]}")
                f.write("\n")
        
        f.write("-" * 50 + "\n")