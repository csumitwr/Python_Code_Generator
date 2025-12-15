import time
from tasks import run_task

# ---------------- BENCHMARK ----------------

BENCHMARK_TASKS = [
    ("DSA", "Given [1,2,3,4,5] and k=7, print the length of the longest contiguous subarray with sum <= k."),
    ("DSA", "Given s='anagram' and t='nagaram', print True if t is an anagram of s."),
    ("DSA", "Given the string 'leetcode', print the index of the first non-repeating character."),
    ("DSA", "Group the anagrams in ['eat','tea','tan','ate','nat','bat'] and print the result."),
    ("DSA", "Given nums=[2,7,11,15] and target=9, print the two indices."),
    ("Algo", "Given [10,9,2,5,3,7,101,18], print the length of LIS."),
    ("Algo", "Given integer 16, print True if it is a power of two."),
    ("IO", "Create scores.csv with ('Alice',90),('Bob',80),('Alice',70),('Bob',85). Print average score per name."),
    ("Plot", "Plot numbers 1 to 10 vs their squares and save the figure."),
    ("Plot", "Generate 500 random numbers and plot a histogram, save it."),
]

def run_benchmark(text_gen):
    """
    Runs all benchmark tasks and returns a summary string.
    """
    results = []

    for _, task in BENCHMARK_TASKS:
        start = time.time()
        res = run_task(task, text_gen)
        elapsed = time.time() - start
        results.append((res["status"].startswith("SUCCESS"), elapsed))

    total = len(results)
    success = sum(1 for ok, _ in results if ok)

    return (
        f"Total tasks: {total}\n"
        f"Eventual success: {100 * success / total:.1f}%\n"
        f"Failure rate: {100 * (total - success) / total:.1f}%\n"
        f"Average runtime: {sum(t for _, t in results) / total:.2f} s"
    )