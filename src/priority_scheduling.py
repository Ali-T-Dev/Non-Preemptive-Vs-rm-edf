def priority_scheduling(processes):
    current_time = 0
    completed = []
    timeline = []
    remaining = processes.copy()

    while remaining:
        available = [
            process for process in remaining
            if process["arrival"] <= current_time
        ]

        if not available:
            next_arrival = min(
                process["arrival"] for process in remaining
            )

            timeline.append({
                "process": "IDLE",
                "start": current_time,
                "end": next_arrival
            })

            current_time = next_arrival
            continue

        selected = min(
            available,
            key=lambda process: (
                process["priority"],
                process["arrival"],
                process["id"]
            )
        )

        start_time = current_time
        completion_time = start_time + selected["burst"]

        turnaround_time = (
            completion_time - selected["arrival"]
        )

        waiting_time = (
            turnaround_time - selected["burst"]
        )

        response_time = (
            start_time - selected["arrival"]
        )

        completed.append({
            "id": selected["id"],
            "arrival": selected["arrival"],
            "burst": selected["burst"],
            "priority": selected["priority"],
            "start": start_time,
            "completion": completion_time,
            "turnaround": turnaround_time,
            "waiting": waiting_time,
            "response": response_time,
        })

        timeline.append({
            "process": selected["id"],
            "start": start_time,
            "end": completion_time
        })

        current_time = completion_time
        remaining.remove(selected)

    return completed, timeline


def main():
    print("=" * 65)
    print(" NON-PREEMPTIVE PRIORITY SCHEDULING ")
    print("=" * 65)

    processes = []

    while True:
        try:
            count = int(input("Enter number of processes: "))

            if count > 0:
                break

            print("Number of processes must be positive.")

        except ValueError:
            print("Please enter a valid integer.")

    for i in range(count):
        print(f"\nProcess P{i + 1}")

        while True:
            try:
                arrival = int(input("Arrival Time: "))
                burst = int(input("Burst Time: "))
                priority = int(input("Priority: "))

                if arrival < 0:
                    print("Arrival Time cannot be negative.")
                    continue

                if burst <= 0:
                    print("Burst Time must be greater than zero.")
                    continue

                if priority < 0:
                    print("Priority cannot be negative.")
                    continue

                break

            except ValueError:
                print("Please enter valid integers.")

        processes.append({
            "id": f"P{i + 1}",
            "arrival": arrival,
            "burst": burst,
            "priority": priority
        })

    completed, timeline = priority_scheduling(processes)

    print("\n" + "=" * 95)
    print("PROCESS SCHEDULING RESULTS")
    print("=" * 95)

    print(
        f"{'Process':<10}"
        f"{'Arrival':<10}"
        f"{'Burst':<10}"
        f"{'Priority':<10}"
        f"{'Start':<10}"
        f"{'Finish':<10}"
        f"{'Turnaround':<13}"
        f"{'Waiting':<10}"
        f"{'Response':<10}"
    )

    print("-" * 95)

    for p in completed:
        print(
            f"{p['id']:<10}"
            f"{p['arrival']:<10}"
            f"{p['burst']:<10}"
            f"{p['priority']:<10}"
            f"{p['start']:<10}"
            f"{p['completion']:<10}"
            f"{p['turnaround']:<13}"
            f"{p['waiting']:<10}"
            f"{p['response']:<10}"
        )

    print("\nCPU TIMELINE")
    print("-" * 40)

    for item in timeline:
        print(
            f"{item['start']} -> {item['end']}: "
            f"{item['process']}"
        )

    total_runtime = timeline[-1]["end"] if timeline else 0
    busy_time = sum(p["burst"] for p in completed)
    idle_time = total_runtime - busy_time

    avg_waiting = sum(
        p["waiting"] for p in completed
    ) / len(completed)

    avg_turnaround = sum(
        p["turnaround"] for p in completed
    ) / len(completed)

    avg_response = sum(
        p["response"] for p in completed
    ) / len(completed)

    cpu_utilization = (
        busy_time / total_runtime * 100
        if total_runtime > 0 else 0
    )

    print("\n" + "=" * 50)
    print("PERFORMANCE SUMMARY")
    print("=" * 50)

    print(f"Total Runtime: {total_runtime}")
    print(f"CPU Busy Time: {busy_time}")
    print(f"CPU Idle Time: {idle_time}")
    print(f"CPU Utilization: {cpu_utilization:.2f}%")
    print(f"Average Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print(f"Average Response Time: {avg_response:.2f}")


if __name__ == "__main__":
    main()