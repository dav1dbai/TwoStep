from dotenv import load_dotenv
from openai import OpenAI
import time
import re
import os
import certifi

load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()
client = OpenAI()

def query(prompt_text, system_text=None, model="gpt-4o"):
    server_flag = 0
    server_cnt = 0
    # import ipdb; ipdb.set_trace()
    while server_cnt < 3:
        try:
            match model:
                case "gpt-4":
                    response = client.chat.completions.create(model="gpt-4",
                    temperature=0,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    messages=[
                        {"role": "system", "content": system_text},
                        {"role": "user", "content": prompt_text},
                    ])
                    result_text = response.choices[0].message.content
                case "gpt-4o":
                    response = client.chat.completions.create(model="gpt-4o",
                    temperature=0,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    messages=[
                        {"role": "system", "content": system_text},
                        {"role": "user", "content": prompt_text},
                    ])
                    result_text = response.choices[0].message.content
                case "o1-mini":
                    response = client.chat.completions.create(model="o1-mini",
                    messages=[
                        {"role": "user", "content": prompt_text},
                    ])
                    result_text = response.choices[0].message.content
                case "o1-preview":
                    response = client.chat.completions.create(model="o1-preview",
                    messages=[
                        {"role": "user", "content": prompt_text},
                    ])
                    result_text = response.choices[0].message.content
                case _:
                    raise ValueError(f"Unsupported model: {model}")
            server_flag = 1
            if server_flag:
                break
        except Exception as e:
            server_cnt += 1
            print("response", response)
            print(e)
    return result_text

import re

def clean_pddl_goal(goal_text):
    # Remove any leading/trailing whitespace
    goal_text = goal_text.strip()

    # Remove empty parentheses
    goal_text = re.sub(r'\(\s*\)', '', goal_text)

    # Remove any consecutive whitespace
    goal_text = re.sub(r'\s+', ' ', goal_text)

    # Remove redundant :goal tags and unnecessary parentheses
    goal_text = re.sub(r'\(:goal\s*\(\s*:goal', '(:goal', goal_text)

    # Ensure proper formatting for 'and' operator
    goal_text = re.sub(r'\(\s*and\s*\)', '', goal_text)  # Remove empty 'and'
    goal_text = re.sub(r'\(\s*and\s+([^()]+)\)', r'(\1)', goal_text)  # Remove unnecessary 'and' with single predicate

    goal_text = goal_text.replace('lisp', '')
    # Remove any triple backticks
    goal_text = goal_text.replace('```', '')

    # Ensure ':goal' is present and properly formatted
    if not goal_text.lstrip('(').startswith(':goal'):
        goal_text = f'(:goal {goal_text.lstrip("(")})'
    else:
        # Ensure there's only one set of parentheses around the entire goal
        goal_text = re.sub(r'^\(:goal\s*\((.*)\)\s*\)$', r'(:goal \1)', goal_text)

    # Balance parentheses
    # open_count = goal_text.count('(')
    # close_count = goal_text.count(')')
    # if open_count > close_count:
    #     goal_text += ')' * (open_count - close_count)
    #elif close_count > open_count:
        #goal_text = goal_text.rstrip(')')  # Remove extra closing parentheses

    # Final check to ensure no trailing parentheses
    goal_text = goal_text.rstrip()
    while goal_text.endswith(')') and goal_text.count('(') < goal_text.count(')'):
        goal_text = goal_text[:-1].rstrip()

    # Fix double-wrapped and clauses
    goal_text = re.sub(r'\(\s*\((and\s+.*?)\)\s*\)', r'(\1)', goal_text)

    return goal_text

def get_pddl_goal(expt_path, args, helper_subgoal, log_file):
    # taken from (LLM+P), create the problem PDDL given the context
    context_nl_filename = f"./domains/{args.domain}/p{args.task_id}.nl"
    with open(context_nl_filename, 'r') as f:
        context_nl = f.read()
    #natural language plan
    context_nl = 'Your goal is to' + context_nl.split('Your goal is to')[-1]
    #print("context_nl", context_nl)
    context_pddl_filename = f"./domains/{args.domain}/p{args.task_id}.pddl"
    with open(context_pddl_filename, 'r') as f:
        context_pddl = f.read()
    context_pddl_init, context_pddl_goal = context_pddl.split('(:goal')
    context_pddl_goal = f'(\n{context_pddl_goal.strip()[:-1]}'

    pddl_problem_filename_arr = []
    
    pddl_problem_filename = f""
    system_text = 'I want you to solve planning problems. Provide me with the PDDL goal that describes the new planning goal directly without further explanations— using only the terminology or predicates defined in the domain, or logical operators appropriate to PDDL. Make sure to provide only non-conflicting, necessary, and final goal conditions mentioned in the given goal.'

    start=time.time()

    for i in range(1, args.num_agents):

        pddl_problem_filename = f"./{expt_path}/p{args.task_id}_{i}.pddl"

        prompt_text = f"The PDDL problem and its initial conditions are given as: \n{context_pddl_init.strip()} \n\n" + \
                    f"An example planning goal for this problem:  \n{context_nl.strip()} \n\n\n" + \
                    f"The PDDL goal for the example planning goal:  \n{context_pddl_goal.strip()} \n\n\n" + \
                    f"New planning goal for the same problem:\n Your goal is: {helper_subgoal[i-1].strip()} \n\n" + \
                    f'The PDDL goal for the new planning goal:\n'

        #print(f"agent {i} prompt \n", prompt_text)
        # import ipdb; ipdb.set_trace()
        # print("\n natural language to pddl prompt \n", prompt_text)
        # keep this to 4o
        print("prompt_text", prompt_text)
        pddl_goal = query(prompt_text, system_text=system_text, model='gpt-4o')
        # import ipdb; ipdb.set_trace()
        # remove undefined goal conditions using domain predicate list
        if args.domain == 'tyreworld':
            pddl_goal = pddl_goal.replace('(empty hands)', '').replace('(empty-hand)', '').replace('(empty-hands)', '').replace('empty hand', '')
        #print("old",pddl_goal)
        pddl_goal = clean_pddl_goal(pddl_goal)
        print("cleaned", pddl_goal)
        with open(log_file, 'a+') as f:
            f.write(f"\n\n{pddl_goal}")
        with open(pddl_problem_filename, 'w') as f:
            f.write(context_pddl_init + pddl_goal + ')')

        pddl_problem_filename_arr.append(pddl_problem_filename)
    
    end = time.time()-start
    return pddl_problem_filename_arr, end