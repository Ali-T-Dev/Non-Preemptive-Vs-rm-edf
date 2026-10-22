# CPU Scheduling Algorithms in Python

A Python project that implements and compares CPU scheduling algorithms using periodic tasks. The project demonstrates how different scheduling strategies select jobs, manage CPU execution, and calculate scheduling performance metrics.

## 📌 Project Overview

This project contains implementations of three CPU scheduling algorithms:

1. **Non-Preemptive Priority Scheduling**
2. **Rate Monotonic (RM) Scheduling**
3. **Earliest Deadline First (EDF) Scheduling**

The combined simulator runs all three algorithms using the same task definitions and simulation length, making it easier to compare their scheduling decisions and performance.

## 🚀 Features

- Periodic task generation.
- Automatic job numbering for each task.
- CPU scheduling timeline similar to a Gantt chart.
- Preemptive and non-preemptive scheduling strategies.
- Job completion and unfinished-job tracking.
- Deadline miss calculation.
- CPU busy time and idle time.
- CPU utilization percentage.
- Average waiting time.
- Average turnaround time.
- Average response time.
- Timeline consistency check in the combined simulator.
- Input validation for positive integer values.

## 🧠 Implemented Algorithms

### 1. Non-Preemptive Priority Scheduling

Each ready job is assigned a priority. The job with the highest priority is selected for execution.

In this project, **a smaller priority number represents a higher priority**.

Once a job starts executing, it continues until it finishes or the simulation ends. A newly released job with a higher priority does not interrupt the currently running job.

If multiple ready jobs have the same priority, the simulator uses their release times and task identifiers to break ties.

### 2. Rate Monotonic (RM) Scheduling

Rate Monotonic is a fixed-priority, preemptive scheduling algorithm designed for periodic real-time tasks.

The task with the shortest period receives the highest priority.

- Shorter period means higher priority.
- Longer period means lower priority.
- A newly released higher-priority task can preempt a currently running lower-priority task.

The RM implementation in this project assumes **implicit deadlines**, meaning each task's relative deadline is equal to its period.

### 3. Earliest Deadline First (EDF) Scheduling

Earliest Deadline First is a dynamic-priority, preemptive scheduling algorithm.

At each scheduling decision, the ready job with the earliest absolute deadline is selected.

The absolute deadline of a job is calculated as:

`Absolute Deadline = Release Time + Relative Deadline`

Unlike RM, EDF does not assign a fixed priority based on the task period. The scheduling order can change as new jobs are released and their deadlines become relevant.

## 📂 Project Structure

```text
Non-Preemptive-Vs-rm&edf/
│
├── scheduling_comparison.py
├── priority_scheduling.py
├── rate_monotonic.py
├── earliest_deadline_first.py
└── README.md
```

### File Descriptions

| File | Description |
|---|---|
| `scheduling_comparison.py` | Runs Non-Preemptive Priority, RM, and EDF using shared task inputs. |
| `priority_scheduling.py` | Standalone implementation of Non-Preemptive Priority Scheduling for processes with arrival times. |
| `rate_monotonic.py` | Compares RM scheduling with Non-Preemptive Priority using periodic tasks. |
| `earliest_deadline_first.py` | Compares EDF scheduling with Non-Preemptive Priority using periodic tasks. |
| `README.md` | Project documentation. |

## ⚙️ Requirements

- Python 3.8 or later
- A terminal or command prompt

The project uses Python's standard library and does not require external packages.

## ▶️ How to Run

Clone the repository or download the project files.

Open a terminal in the project directory:

```bash
cd Non-Preemptive-Vs-rm&edf
```

Run the combined simulator:

```bash
python scheduling_comparison.py
```

To run the standalone implementations, use:

```bash
python priority_scheduling.py
```

```bash
python rate_monotonic.py
```

```bash
python earliest_deadline_first.py
```

Depending on your environment, you may need to use `python3` instead of `python`.

## 📝 Input Parameters

### Combined Simulator

The `scheduling_comparison.py` file requests the following information:

| Parameter | Description |
|---|---|
| Number of tasks | Number of periodic tasks to simulate. |
| Period | Time interval between consecutive releases of a task. |
| Execution Time | CPU time required by each job of a task. |
| Priority | Priority used by Non-Preemptive Priority Scheduling. |
| Relative Deadline | Time allowed from a job's release until its deadline for EDF. |
| Simulation Length | Total duration of the simulation. |

For the current implementation, execution time must be less than or equal to the task period.

### Example Input

```text
Number of tasks: 3

Task T1
Period: 5
Execution time: 1
Priority: 3
Relative deadline: 4

Task T2
Period: 7
Execution time: 2
Priority: 1
Relative deadline: 6

Task T3
Period: 10
Execution time: 1
Priority: 2
Relative deadline: 8

Simulation length: 30
```

## 📊 Performance Metrics

The simulators calculate the following metrics.

### Turnaround Time

The total time between a job's release and completion.

`Turnaround Time = Completion Time - Release Time`

### Waiting Time

The time a job spends waiting for CPU execution.

`Waiting Time = Turnaround Time - Execution Time`

### Response Time

The time between a job's release and its first CPU execution.

`Response Time = First Start Time - Release Time`

For preemptive algorithms, response time is based on the first time the job starts, not the time it resumes after preemption.

### CPU Utilization

The percentage of simulation time during which the CPU is executing jobs.

`CPU Utilization = (CPU Busy Time / Simulation Length) × 100`

### Deadline Misses

A job is counted as a deadline miss if its deadline falls within the simulation horizon and the job has not completed by that deadline.

## 📈 Output

For each algorithm, the combined simulator displays:

- Gantt-style CPU timeline.
- Per-job release, execution, priority, deadline, start, and completion times.
- Turnaround, waiting, and response times.
- Number of jobs released and completed.
- Number of unfinished jobs.
- Number of deadline misses.
- CPU busy time and idle time.
- CPU utilization.
- Average scheduling metrics.
- Timeline consistency status.

The timeline consistency check verifies that the displayed timeline covers the complete simulation interval and that CPU busy time plus idle time equals the simulation length.

## 🔍 Comparing the Algorithms

The project can be used to investigate how scheduling policies affect job execution.

| Algorithm | Priority Strategy | Preemptive? | Main Scheduling Criterion |
|---|---|---|---|
| Non-Preemptive Priority | Fixed user-defined priority | No | Highest-priority ready job |
| Rate Monotonic (RM) | Fixed task priority | Yes | Shortest task period |
| Earliest Deadline First (EDF) | Dynamic job priority | Yes | Earliest absolute deadline |

The algorithms may produce identical timelines for some task sets. This does not necessarily indicate an implementation error. Their behavior depends on task periods, execution times, priorities, deadlines, and release times.

For a meaningful comparison, experiment with different valid task parameters and compare the resulting timelines and performance metrics.

## ⚠️ Assumptions and Limitations

- Task periods and execution times are positive integers.
- The periodic task simulators generate jobs whose release times are earlier than the simulation end.
- Execution time must not exceed the task period in the current implementations.
- The combined simulator uses the same periodic task definitions for all three algorithms.
- RM uses implicit deadlines equal to task periods.
- EDF uses the relative deadlines entered by the user.
- Non-Preemptive Priority does not interrupt a running job.
- RM and EDF can interrupt a running job when a scheduling decision at a job-release event selects another job.
- The simulators do not model context-switch overhead, blocking, resource sharing, or multicore execution.
- The simulation is a simplified educational model of CPU scheduling.

## 🎓 Project Purpose

This project was developed as an educational exercise to understand operating-system scheduling concepts, implement scheduling algorithms in Python, and compare their behavior through simulation.

It is suitable for university assignments, algorithm demonstrations, and introductory real-time scheduling experiments.

## 👨‍💻 Author

**Ali Naviani**

## 📄 License

This project is available for educational and learning purposes. Add a specific open-source license file if you intend to distribute it under a formal license.
