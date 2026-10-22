
def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Enter a positive integer.")
        except ValueError:
            print("Invalid input. Try again.")


def create_jobs(tasks, limit):
    jobs = []

    for task in tasks:
        release = 0
        number = 1

        while release < limit:
            jobs.append({
                "id": f"{task['id']}-{number}",
                "task": task["id"],
                "release": release,
                "burst": task["execution"],
                "remaining": task["execution"],
                "priority": task["priority"],
                "period": task["period"],
                "deadline": release + task["deadline"],
                "start": None,
                "finish": None,
            })

            release += task["period"]
            number += 1

    return jobs


def add_segment(timeline, start, end, name):
    if end <= start:
        return

    # Merge adjacent segments belonging to the same job.
    if (
        timeline
        and timeline[-1]["job"] == name
        and timeline[-1]["end"] == start
    ):
        timeline[-1]["end"] = end
    else:
        timeline.append({
            "start": start,
            "end": end,
            "job": name,
        })


def simulate(tasks, limit, algorithm):
    jobs = create_jobs(tasks, limit)
    timeline = []
    time = 0

    rm_rank = {
        task["id"]: rank
        for rank, task in enumerate(
            sorted(tasks, key=lambda item: (item["period"], item["id"])),
            start=1,
        )
    }

    while time < limit:
        ready = [
            job for job in jobs
            if job["release"] <= time and job["remaining"] > 0
        ]

        if not ready:
            future = [
                job["release"] for job in jobs
                if job["release"] > time and job["remaining"] > 0
            ]

            next_time = min(future) if future else limit
            next_time = min(next_time, limit)
            add_segment(timeline, time, next_time, "IDLE")
            time = next_time
            continue

        if algorithm == "Priority":
            selected = min(
                ready,
                key=lambda job: (
                    job["priority"], job["release"], job["task"]
                ),
            )

        elif algorithm == "RM":
            selected = min(
                ready,
                key=lambda job: (
                    rm_rank[job["task"]], job["release"], job["task"]
                ),
            )

        else:  # EDF
            selected = min(
                ready,
                key=lambda job: (
                    job["deadline"], job["release"], job["task"]
                ),
            )

        if selected["start"] is None:
            selected["start"] = time

        if algorithm == "Priority":
            # Non-preemptive: run until completion or simulation end.
            end = min(time + selected["remaining"], limit)
        else:
            # Preemptive: reconsider scheduling at the next release.
            future = [
                job["release"] for job in jobs
                if job["release"] > time
            ]
            next_release = min(future) if future else limit
            end = min(
                time + selected["remaining"],
                next_release,
                limit,
            )

        executed = end - time
        add_segment(timeline, time, end, selected["id"])
        selected["remaining"] -= executed
        time = end

        if selected["remaining"] == 0:
            selected["finish"] = time

    return jobs, timeline


def print_results(name, jobs, timeline, limit):
    print("\n" + "=" * 90)
    print(name.center(90))
    print("=" * 90)

    print("\nGantt Timeline:")
    for segment in timeline:
        print(
            f"{segment['start']:>4} -> "
            f"{segment['end']:<4}: {segment['job']}"
        )

    print("\nJob Details:")
    print(
        f"{'Job':<9}{'Release':>8}{'Burst':>7}"
        f"{'Priority':>9}{'Deadline':>10}{'Start':>8}"
        f"{'Finish':>8}{'TAT':>7}{'Wait':>7}"
        f"{'Response':>10}{'Status':>12}"
    )
    print("-" * 105)

    completed = [job for job in jobs if job["finish"] is not None]

    for job in jobs:
        start = job["start"]
        finish = job["finish"]

        tat = finish - job["release"] if finish is not None else None
        waiting = tat - job["burst"] if tat is not None else None
        response = start - job["release"] if start is not None else None
        status = "Completed" if finish is not None else "Unfinished"

        def fmt(value):
            return "-" if value is None else str(value)

        print(
            f"{job['id']:<9}{job['release']:>8}{job['burst']:>7}"
            f"{job['priority']:>9}{job['deadline']:>10}"
            f"{fmt(start):>8}{fmt(finish):>8}"
            f"{fmt(tat):>7}{fmt(waiting):>7}"
            f"{fmt(response):>10}{status:>12}"
        )

    busy = sum(
        part["end"] - part["start"]
        for part in timeline if part["job"] != "IDLE"
    )
    idle = sum(
        part["end"] - part["start"]
        for part in timeline if part["job"] == "IDLE"
    )

    misses = sum(
        1 for job in jobs
        if job["deadline"] <= limit
        and (
            job["finish"] is None
            or job["finish"] > job["deadline"]
        )
    )

    waiting_times = [
        job["finish"] - job["release"] - job["burst"]
        for job in completed
    ]
    turnaround_times = [
        job["finish"] - job["release"] for job in completed
    ]
    response_times = [
        job["start"] - job["release"] for job in completed
    ]

    def average(values):
        return sum(values) / len(values) if values else 0

    utilization = busy / limit * 100

    print("\nSummary:")
    print(f"Jobs released:          {len(jobs)}")
    print(f"Jobs completed:         {len(completed)}")
    print(f"Jobs unfinished:        {len(jobs) - len(completed)}")
    print(f"Deadline misses:        {misses}")
    print(f"CPU busy time:          {busy}")
    print(f"CPU idle time:          {idle}")
    print(f"CPU utilization:        {utilization:.2f}%")
    print(f"Average waiting time:   {average(waiting_times):.2f}")
    print(f"Average turnaround:     {average(turnaround_times):.2f}")
    print(f"Average response:       {average(response_times):.2f}")

    # Check that the timeline covers the whole simulation.
    timeline_duration = sum(
        part["end"] - part["start"] for part in timeline
    )

    if timeline_duration == limit and busy + idle == limit:
        print("Timeline consistency:   OK")
    else:
        print("WARNING: Timeline/statistics mismatch!")


def main():
    print("=" * 60)
    print("CPU SCHEDULING COMPARISON")
    print("=" * 60)

    count = get_positive_int("Number of tasks: ")
    tasks = []

    for index in range(1, count + 1):
        print(f"\nTask T{index}")

        period = get_positive_int("Period: ")
        execution = get_positive_int("Execution time: ")

        while execution > period:
            print("Execution time must be <= period.")
            execution = get_positive_int("Execution time: ")

        priority = get_positive_int(
            "Priority for Non-Preemptive Priority: "
        )
        deadline = get_positive_int("Relative deadline for EDF: ")

        tasks.append({
            "id": f"T{index}",
            "period": period,
            "execution": execution,
            "priority": priority,
            "deadline": deadline,
        })

    limit = get_positive_int("\nSimulation length: ")

    algorithms = [
        ("Priority", "1. NON-PREEMPTIVE PRIORITY"),
        ("RM", "2. RATE MONOTONIC (RM)"),
        ("EDF", "3. EARLIEST DEADLINE FIRST (EDF)"),
    ]

    for algorithm, title in algorithms:
        jobs, timeline = simulate(tasks, limit, algorithm)
        print_results(title, jobs, timeline, limit)


if __name__ == "__main__":
    main()
