import random
import subprocess
import os
import shutil

def evaluate_performance(code_path):
    """Run the AI script and get its performance score."""
    try:
        result = subprocess.run(['python', code_path], capture_output=True, text=True, timeout=5)
        output = result.stdout.strip()
        return float(output) if output.replace('.', '', 1).isdigit() else 0
    except Exception as e:
        print(f"Error evaluating performance: {e}")
        return 0

def mutate_code(code_path):
    """Modify the existing AI code to introduce improvements."""
    with open(code_path, 'r') as file:
        lines = file.readlines()
    
    if not lines:
        return
    
    mutation_point = random.randint(0, len(lines) - 1)
    mutation_type = random.choice(['modify', 'insert', 'delete'])
    
    if mutation_type == 'modify':
        lines[mutation_point] = '# Mutated line\n'  # Replace with actual improvement logic
    elif mutation_type == 'insert':
        lines.insert(mutation_point, '# New improvement\n')
    elif mutation_type == 'delete' and len(lines) > 1:
        del lines[mutation_point]
    
    new_code_path = f"mutated_{code_path}"
    with open(new_code_path, 'w') as file:
        file.writelines(lines)
    
    return new_code_path

def evolve_ai(initial_code_path, iterations=10):
    """Main loop to iteratively improve the AI code."""
    best_code = initial_code_path
    best_score = evaluate_performance(best_code)
    
    for _ in range(iterations):
        new_code = mutate_code(best_code)
        if not new_code:
            continue
        
        new_score = evaluate_performance(new_code)
        if new_score > best_score:
            best_code, best_score = new_code, new_score
            shutil.copy(new_code, 'best_ai.py')  # Save best version
            print(f"Improved AI with score: {best_score}")
        
        os.remove(new_code)  # Clean up temporary files
    
    print("Final best AI stored in best_ai.py")

# Example: Initial AI code
with open('ai.py', 'w') as f:
    f.write("print(1.0)  # Initial simple AI output")

evolve_ai('ai.py', iterations=5)
