
def get_int(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
            print(f"Enter a value greater than or equal to {minimum}.")
        except ValueError:
            print("Please enter a valid integer.")


def create_periodic_jobs(tasks, simulation_length):
    jobs = []

    for task_index, task in enumerate(tasks):
        release = 0
        job_number = 1

        while release < simulation_length:
            jobs.append({
                "id": f'{task["id"]}-{job_number}',
                "task_id": task["id"],
                "task_index": task_index,
                "release": release,
                "burst": task["execution"],
                "remaining": task["execution"],
                "priority": task["priority"],
                "period": task["period"],
                "deadline": release + task["relative_deadline"],
                "start": None,
                "completion": None,
            })

            release += task["period"]
            job_number += 1

    return jobs


def append_segment(timeline, start, end, label):
    if end <= start:
        return

    if (
        timeline
        and timeline[-1]["end"] == start
        and timeline[-1]["label"] == label
    ):
        timeline[-1]["end"] = end
    else:
        timeline.append({
            "start": start,
            "end": end,
            "label": label,
        })


def schedule_edf(jobs, simulation_length):
    time = 0
    timeline = []

    while time < simulation_length:
        ready = [
            job for job in jobs
            if job["release"] <= time
            and job["remaining"] > 0
        ]

        if not ready:
            future_releases = [
                job["release"] for job in jobs
                if time < job["release"] < simulation_length
            ]

            next_time = min(future_releases, default=simulation_length)
            append_segment(timeline, time, next_time, "IDLE")
            time = next_time
            continue

        selected = min(
            ready,
            key=lambda job: (
                job["deadline"],
                job["release"],
                job["task_index"],
                int(job["id"].split("-")[1]),
            ),
        )

        future_releases = [
            job["release"] for job in jobs
            if time < job["release"] < simulation_length
        ]

        next_release = min(future_releases, default=simulation_length)
        end = min(
            time + selected["remaining"],
            next_release,
            simulation_length,
        )

        if selected["start"] is None:
            selected["start"] = time

        append_segment(timeline, time, end, selected["id"])

        executed = end - time
        selected["remaining"] -= executed
        time = end

        if selected["remaining"] == 0:
            selected["completion"] = time

    return timeline


def schedule_non_preemptive_priority(jobs, simulation_length):
    time = 0
    timeline = []

    while time < simulation_length:
        ready = [
            job for job in jobs
            if job["release"] <= time
            and job["remaining"] > 0
        ]

        if not ready:
            future_releases = [
                job["release"] for job in jobs
                if time < job["release"] < simulation_length
            ]

            next_time = min(future_releases, default=simulation_length)
            append_segment(timeline, time, next_time, "IDLE")
            time = next_time
            continue

        selected = min(
            ready,
            key=lambda job: (
                job["priority"],
                job["release"],
                job["task_index"],
                int(job["id"].split("-")[1]),
            ),
        )

        if selected["start"] is None:
            selected["start"] = time

        end = min(
            time + selected["remaining"],
            simulation_length,
        )

        append_segment(timeline, time, end, selected["id"])

        selected["remaining"] -= end - time
        time = end

        if selected["remaining"] == 0:
            selected["completion"] = time

    return timeline


def print_timeline(title, timeline):
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    for segment in timeline:
        print(
            f'{segment["start"]} -> {segment["end"]}: '
            f'{segment["label"]}'
        )


def print_results(title, jobs, timeline, simulation_length):
    completed = [
        job for job in jobs
        if job["completion"] is not None
    ]

    deadline_misses = [
        job for job in jobs
        if job["deadline"] <= simulation_length
        and (
            job["completion"] is None
            or job["completion"] > job["deadline"]
        )
    ]

    busy_time = sum(
        segment["end"] - segment["start"]
        for segment in timeline
        if segment["label"] != "IDLE"
    )
    idle_time = simulation_length - busy_time
    utilization = busy_time / simulation_length * 100

    print("\n" + "=" * 105)
    print(title)
    print("=" * 105)

    print(
        f'{"Job":<10}{"Release":<10}{"Burst":<9}'
        f'{"Priority":<10}{"Deadline":<10}{"Start":<9}'
        f'{"Finish":<10}{"TAT":<9}{"Waiting":<10}{"Response":<10}'
    )
    print("-" * 105)

    for job in jobs:
        finish = job["completion"]
        start = job["start"]

        if finish is not None:
            turnaround = finish - job["release"]
            waiting = turnaround - job["burst"]
            response = start - job["release"]
        else:
            turnaround = waiting = response = None

        def display(value):
            return "-" if value is None else str(value)

        print(
            f'{job["id"]:<10}'
            f'{job["release"]:<10}'
            f'{job["burst"]:<9}'
            f'{job["priority"]:<10}'
            f'{job["deadline"]:<10}'
            f'{display(start):<9}'
            f'{display(finish):<10}'
            f'{display(turnaround):<9}'
            f'{display(waiting):<10}'
            f'{display(response):<10}'
        )

    print("-" * 105)
    print(f"Jobs released: {len(jobs)}")
    print(f"Jobs completed: {len(completed)}")
    print(f"Jobs unfinished: {len(jobs) - len(completed)}")
    print(f"Deadline misses: {len(deadline_misses)}")
    print(f"CPU busy time: {busy_time}")
    print(f"CPU idle time: {idle_time}")
    print(f"CPU utilization: {utilization:.2f}%")

    if completed:
        avg_waiting = sum(
            job["completion"] - job["release"] - job["burst"]
            for job in completed
        ) / len(completed)

        avg_turnaround = sum(
            job["completion"] - job["release"]
            for job in completed
        ) / len(completed)

        avg_response = sum(
            job["start"] - job["release"]
            for job in completed
        ) / len(completed)

        print(f"Average Waiting Time: {avg_waiting:.2f}")
        print(f"Average Turnaround Time: {avg_turnaround:.2f}")
        print(f"Average Response Time: {avg_response:.2f}")
    else:
        print("No jobs completed; average times are unavailable.")


def main():
    print("=" * 65)
    print(" EARLIEST DEADLINE FIRST vs NON-PREEMPTIVE PRIORITY")
    print("=" * 65)

    count = get_int("Enter number of periodic tasks: ")
    tasks = []

    for i in range(count):
        print(f"\nTask T{i + 1}")

        period = get_int("Period: ")
        execution = get_int("Execution Time: ")

        while execution > period:
            print("Execution Time should not exceed Period for this input.")
            execution = get_int("Execution Time: ")

        relative_deadline = get_int("Relative Deadline: ")
        priority = get_int("Priority for comparison: ")

        tasks.append({
            "id": f"T{i + 1}",
            "period": period,
            "execution": execution,
            "relative_deadline": relative_deadline,
            "priority": priority,
        })

    simulation_length = get_int("Simulation length: ")

    print("\nEDF uses earliest absolute Deadline = highest priority.")

    edf_jobs = create_periodic_jobs(tasks, simulation_length)
    edf_timeline = schedule_edf(edf_jobs, simulation_length)

    priority_jobs = create_periodic_jobs(tasks, simulation_length)
    priority_timeline = schedule_non_preemptive_priority(
        priority_jobs, simulation_length
    )

    print_timeline("EARLIEST DEADLINE FIRST TIMELINE", edf_timeline)
    print_results(
        "EARLIEST DEADLINE FIRST RESULTS",
        edf_jobs,
        edf_timeline,
        simulation_length,
    )

    print_timeline(
        "NON-PREEMPTIVE PRIORITY TIMELINE",
        priority_timeline,
    )
    print_results(
        "NON-PREEMPTIVE PRIORITY RESULTS",
        priority_jobs,
        priority_timeline,
        simulation_length,
    )


if __name__ == "__main__":
    main()
