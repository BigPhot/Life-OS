import yaml
from typing import Dict, List, Any
import math

def parse_tasks_from_yaml(yaml_file_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Parse tasks from a YAML file and extract specific criteria values.
    
    Args:
        yaml_file_path (str): Path to the YAML file containing tasks
        
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary with task names as keys and criteria as values
        Format: {
            "task_name": {
                "corePercentage": int,
                "effortComplexity": int,
                "organizationValue": int,
                "dueInDays": int
            }
        }
    """
    try:
        with open(yaml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        if not data or 'tasks' not in data:
            print("No tasks found in YAML file")
            return {}
        
        tasks_dict = {}
        
        for task in data['tasks']:
            task_title = task.get('title', 'Unknown Task')
            
            # Extract corePercentage from coreAlignment
            core_percentage = task.get('coreAlignment', {}).get('percentage', 0)
            
            # Extract effortComplexity from magnitude
            effort_complexity = task.get('magnitude', {}).get('effortComplexity', 0)
            
            # Extract organization value
            organization_value = task.get('organization', {}).get('value', 0)
            
            # Extract dueInDays from timeframe
            due_in_days = task.get('timeframe', {}).get('dueInDays', 0)
            
            tasks_dict[task_title] = {
                'corePercentage': core_percentage,
                'effortComplexity': effort_complexity,
                'organizationValue': organization_value,
                'dueInDays': due_in_days
            }
        
        return tasks_dict
        
    except FileNotFoundError:
        print(f"Error: File '{yaml_file_path}' not found")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

def print_tasks_summary(tasks_dict: Dict[str, Dict[str, Any]]) -> None:
    """
    Print a formatted summary of all tasks and their criteria.
    
    Args:
        tasks_dict (Dict[str, Dict[str, Any]]): Dictionary of tasks and criteria
    """
    if not tasks_dict:
        print("No tasks to display")
        return
    
    print(f"\n{'='*80}")
    print(f"{'TASK SUMMARY':^80}")
    print(f"{'='*80}")
    
    for task_name, criteria in tasks_dict.items():
        print(f"\nTask: {task_name}")
        print(f"  Core Alignment: {criteria['corePercentage']}%")
        print(f"  Effort Complexity: {criteria['effortComplexity']}")
        print(f"  Organization Value: {criteria['organizationValue']}")
        print(f"  Due In: {criteria['dueInDays']} days")
        print("-" * 60)

def calculate_task_score(criteria: Dict[str, Any], weights: Dict[str, float]) -> float:
    """
    Calculate a weighted linear score for a task based on its criteria.
    
    Args:
        criteria (Dict[str, Any]): Task criteria dictionary
        weights (Dict[str, float]): Weights for each criterion
        
    Returns:
        float: Weighted score for the task
    """
    score = 0.0
    
    # Core percentage (0-100, higher is better)
    core_score = criteria['corePercentage'] / 100.0
    core_weighted = core_score * weights.get('corePercentage', 1.0)
    score += core_weighted
    
    # Effort complexity (0-10, lower is better, so we invert it)
    # Convert to 0-1 scale where 1 is best (lowest effort)
    effort_score = (criteria['effortComplexity']) / 10.0
    effort_weighted = effort_score * weights.get('effortComplexity', 1.0)
    score += effort_weighted
    
    # Organization value (0-10, higher is better)
    # Normalize to 0-1 scale
    org_score = min(criteria['organizationValue'] / 10.0, 1.0)
    org_weighted = org_score * weights.get('organizationValue', 1.0)
    score += org_weighted
    
    # Due in days (urgency factor, lower is better, so we invert it)
    # Convert to 0-1 scale where 1 is most urgent (0 days)
    # Normalize so that lower dueInDays gives higher score, using inverse (1 / (1 + dueInDays))
    # But tasks with no due date (0 days) should be pushed back, not prioritized
    base = 1
    scale = 6.0
    alpha = 0.1
    if criteria['dueInDays'] == 0:
        urgency_score = 0.0  # No due date = lowest urgency priority
    else:
        urgency_score = base + scale * math.exp(-alpha * criteria['dueInDays'])
    
    urgency_weighted = urgency_score * weights.get('dueInDays', 1.0)
    score += urgency_weighted
    
    # Debug printing
    print(f"  DEBUG - Task: {criteria.get('title', 'Unknown')}")
    print(f"    Core: {criteria['corePercentage']}% -> {core_score:.3f} * {weights.get('corePercentage', 1.0):.1f} = {core_weighted:.3f}")
    print(f"    Effort: {criteria['effortComplexity']} -> {effort_score:.3f} * {weights.get('effortComplexity', 1.0):.1f} = {effort_weighted:.3f}")
    print(f"    Org: {criteria['organizationValue']} -> {org_score:.3f} * {weights.get('organizationValue', 1.0):.1f} = {org_weighted:.3f}")
    
    print(f"    Due: {criteria['dueInDays']} days -> {urgency_score:.3f} * {weights.get('dueInDays', 1.0):.1f} = {urgency_weighted:.3f}")
    if criteria['dueInDays'] > 0:
        print(f"      (Equation: {base:.1f} + {scale:.1f} * exp(-{alpha:.1f} * {criteria['dueInDays']}) = {base:.1f} + {scale:.1f} * {math.exp(-alpha * criteria['dueInDays']):.3f} = {urgency_score:.3f})")
    else:
        print(f"      (No due date = 0.0)")
    print(f"    Total Score: {score:.3f}")
    print()
    
    return score

def distribute_scores_to_20ths(task_scores: List[tuple]) -> List[tuple]:
    """
    Distribute task scores into 20 equal parts based on their relative scores.
    
    Args:
        task_scores (List[tuple]): List of (task_name, score) tuples
        
    Returns:
        List[tuple]: List of (task_name, score, parts_of_20, percentage) tuples
    """
    if not task_scores:
        return []
    
    # Calculate total score
    total_score = sum(score for _, score in task_scores)
    
    if total_score == 0:
        return []
    
    # Calculate parts of 20 for each task
    distribution = []
    for task_name, score in task_scores:
        # Calculate percentage of total
        percentage = (score / total_score) * 100
        
        # Calculate parts of 20 (rounded to nearest whole number)
        parts_of_20 = round((score / total_score) * 20)
        
        distribution.append((task_name, score, parts_of_20, percentage))
    
    return distribution

def print_20th_distribution(distribution: List[tuple]) -> None:
    """
    Print the distribution of tasks into 20ths.
    
    Args:
        distribution (List[tuple]): List of (task_name, score, parts_of_20, percentage) tuples
    """
    if not distribution:
        print("No distribution to display")
        return
    
    print(f"\n{'='*80}")
    print(f"{'TASK DISTRIBUTION INTO 20THS':^80}")
    print(f"{'='*80}")
    
    # Sort by parts of 20 (highest first)
    sorted_distribution = sorted(distribution, key=lambda x: x[2], reverse=True)
    
    print(f"\n{'Task':<50} {'Score':<8} {'Parts/20':<10} {'% of Total':<12}")
    print("-" * 80)
    
    total_parts = 0
    for task_name, score, parts, percentage in sorted_distribution:
        print(f"{task_name[:49]:<50} {score:<8.3f} {parts:<10} {percentage:<12.1f}%")
        total_parts += parts
    
    print("-" * 80)
    print(f"{'TOTAL':<50} {'':<8} {total_parts:<10} {'100.0':<12}%")
    
    # Show visual representation
    print(f"\n{'Visual Representation (20 parts)':^80}")
    print("-" * 80)
    
    for task_name, score, parts, percentage in sorted_distribution:
        if parts > 0:
            visual = "█" * parts
            print(f"{task_name[:30]:<30} {visual} ({parts}/20)")
        else:
            print(f"{task_name[:30]:<30} {'·' * 20} (0/20)")
    
    print("-" * 80)

def rank_tasks_by_score(tasks_dict: Dict[str, Dict[str, Any]], weights: Dict[str, float]) -> List[tuple]:
    """
    Rank tasks by their calculated scores.
    
    Args:
        tasks_dict (Dict[str, Dict[str, Any]]): Dictionary of tasks and criteria
        weights (Dict[str, float]): Weights for each criterion
        
    Returns:
        List[tuple]: List of (task_name, score) tuples sorted by score (highest first)
    """
    task_scores = []
    
    for task_name, criteria in tasks_dict.items():
        score = calculate_task_score(criteria, weights)
        task_scores.append((task_name, score))
    
    # Sort by score (highest first)
    task_scores.sort(key=lambda x: x[1], reverse=True)
    return task_scores

def print_ranked_tasks(tasks_dict: Dict[str, Dict[str, Any]], weights: Dict[str, float]) -> None:
    """
    Print tasks ranked by their calculated scores.
    
    Args:
        tasks_dict (Dict[str, Dict[str, Any]]): Dictionary of tasks and criteria
        weights (Dict[str, float]): Weights for each criterion
    """
    ranked_tasks = rank_tasks_by_score(tasks_dict, weights)
    
    print(f"\n{'='*80}")
    print(f"{'TASK RANKING BY SCORE':^80}")
    print(f"{'='*80}")
    
    print(f"\nWeights used:")
    print(f"  Core Alignment: {weights.get('corePercentage', 1.0):.2f}")
    print(f"  Effort Complexity: {weights.get('effortComplexity', 1.0):.2f}")
    print(f"  Organization Value: {weights.get('organizationValue', 1.0):.2f}")
    print(f"  Due In Days: {weights.get('dueInDays', 1.0):.2f}")
    
    print(f"\nRanked Tasks:")
    for i, (task_name, score) in enumerate(ranked_tasks, 1):
        criteria = tasks_dict[task_name]
        print(f"\n{i}. {task_name}")
        print(f"   Score: {score:.3f}")
        print(f"   Core: {criteria['corePercentage']}% | Effort: {criteria['effortComplexity']} | Org: {criteria['organizationValue']} | Due: {criteria['dueInDays']} days")
        print("-" * 60)

if __name__ == "__main__":
    # Example usage
    yaml_file = "example_task.yaml"
    tasks = parse_tasks_from_yaml(yaml_file)
    
    if tasks:
        print(f"Successfully parsed {len(tasks)} tasks from {yaml_file}")
        
        # Display basic task summary
        print_tasks_summary(tasks)
        # Example of custom weights
        print(f"\n{'='*80}")
        print(f"{'CUSTOM WEIGHT EXAMPLE':^80}")
        print(f"{'='*80}")
        
        custom_weights = {
            'corePercentage': 1.2,      # Prioritize core alignment
            'effortComplexity': 2.5,    # Strongly prefer easier tasks
            'organizationValue': 1.1,   # Less emphasis on organization
            'dueInDays': 3.5            # Moderate urgency consideration
        }
        
        print_ranked_tasks(tasks, custom_weights)
        
        # Demonstrate the 20th distribution
        print(f"\n{'='*80}")
        print(f"{'20TH DISTRIBUTION DEMO':^80}")
        print(f"{'='*80}")
        
        # Get the ranked tasks
        ranked_tasks = rank_tasks_by_score(tasks, custom_weights)
        
        # Create distribution into 20ths
        distribution = distribute_scores_to_20ths(ranked_tasks)
        
        # Print the distribution
        print_20th_distribution(distribution)
        
    else:
        print("Failed to parse tasks from YAML file")
