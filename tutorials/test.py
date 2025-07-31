# conda run --live-stream --name biomni_e1 python /home/changhu/Biomni/tutorials/test.py


import os
import sys
from contextlib import redirect_stdout
from biomni.agent import A1
from biomni.llm import get_llm

def run_test():
    api_key = "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"

    if not api_key:
        raise ValueError("OpenRouter API key not found. Please set the OPENROUTER_API_KEY environment variable.")

    print("Step 1: Creating the LLM instance for OpenRouter...")
    try:
        llm_instance = get_llm(
            model="moonshotai/kimi-k2:free",
            source="OpenRouter",
            api_key=api_key
        )
        print("LLM instance created successfully.")
    except Exception as e:
        print(f"Error creating LLM instance: {e}")
        return

    print("\nStep 2: Initializing the BioMni Agent...")
    agent = A1(
        path='./data',
        llm=llm_instance
    )
    print("Agent initialized successfully.")

    tasks = [
        "Plan a CRISPR screen to identify genes that regulate T cell exhaustion, generate 32 genes that maximize the perturbation effect.",
        "Perform scRNA-seq annotation at [PATH] and generate meaningful hypothesis",
        "Predict ADMET properties for this compound: CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n{'='*30}")
        print(f"Executing Task {i}: {task}")
        print(f"{'='*30}")
        try:
            log, final_content = agent.go(task)
            print("\n--- Agent Execution Log ---")
            for entry in log:
                print(entry)
            print("--- End of Log ---")
            print(f"\nTask {i} Final Output:\n{final_content}")
        except Exception as e:
            print(f"An error occurred during task execution: {e}")

if __name__ == "__main__":
    log_file_path = "execution_log.txt"
    print(f"Starting execution. All output will be saved to '{log_file_path}'")

    with open(log_file_path, 'w', encoding='utf-8') as log_file:
        with redirect_stdout(log_file):
            try:
                run_test()
            except Exception as e:
                print(f"\nA critical error occurred: {e}", file=sys.stderr)
                print(f"\nA critical error occurred: {e}")

    print("Execution finished. Log has been saved successfully.")
