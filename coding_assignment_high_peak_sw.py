from bisect import bisect_right

def find_last_non_conflict(jobs, index):
    """
    Returns the index of the last job in 'jobs' that doesn't conflict with jobs[index].
    Consecutive jobs are allowed, so we need the last job with an end time <= current job's start time.
    """
    # Create a list of end times for binary search.
    end_times = [job[1] for job in jobs]
    # bisect_right returns an insertion point; subtract 1 to get the valid index.
    i = bisect_right(end_times, jobs[index][0]) - 1
    return i if i >= 0 else None

def maximize_profit(jobs):
    """
    Uses dynamic programming to determine the maximum profit and the count of jobs selected.
    jobs: List of tuples (start, end, profit), sorted by end time.
    Returns: (max_profit, count_jobs)
    """
    n = len(jobs)
    # dp[i] = (max_profit, count_jobs) using jobs[0...i]
    dp = [None] * n
    dp[0] = (jobs[0][2], 1)  # Only the first job taken

    for i in range(1, n):
        # Option 1: Exclude the current job; carry over the previous best.
        profit_exclude, count_exclude = dp[i-1]
        
        # Option 2: Include the current job.
        current_profit = jobs[i][2]
        current_count = 1
        
        # Find the last job that does not conflict (consecutive jobs are allowed)
        l = find_last_non_conflict(jobs, i)
        if l is not None:
            current_profit += dp[l][0]
            current_count += dp[l][1]
        
        # Choose the option with a higher profit.
        if current_profit > profit_exclude:
            dp[i] = (current_profit, current_count)
        else:
            dp[i] = (profit_exclude, count_exclude)
    
    return dp[-1]

def main():
    # Read the number of jobs
    n = int(input("Enter the number of Jobs\n").strip())
    
    jobs = []
    print("Enter job start time, end time, and earnings")
    for _ in range(n):
        start = int(input().strip())
        end = int(input().strip())
        profit = int(input().strip())
        jobs.append((start, end, profit))
    
    # Calculate the total profit from all jobs.
    total_profit = sum(job[2] for job in jobs)
    
    # Sort the jobs based on their end times.
    jobs.sort(key=lambda job: job[1])
    
    # Use dynamic programming to get the best possible profit and job count for Lokesh.
    lokesh_profit, lokesh_count = maximize_profit(jobs)
    
    # Calculate the number of remaining jobs and the earnings available for other employees.
    tasks_left = n - lokesh_count
    earnings_left = total_profit - lokesh_profit
    
    print("Task:", tasks_left)
    print("Earnings:", earnings_left)

if __name__ == "__main__":
    main()

