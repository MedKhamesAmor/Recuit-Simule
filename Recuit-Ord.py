import random
import math

class JobShopScheduling:
    def __init__(self, jobs):
        self.jobs = jobs
        self.num_machines = max(machine for job in jobs.values() for machine, _ in job) + 1
        self.num_jobs = len(jobs)

    def decode_schedule(self, operation_sequence):
        machine_times = [0] * self.num_machines
        job_times = [0] * (self.num_jobs + 1)
        schedule = []
        makespan = 0

        for job_id, op_num in operation_sequence:
            machine, duration = self.jobs[job_id][op_num]
            start_time = max(machine_times[machine], job_times[job_id])
            end_time = start_time + duration
            machine_times[machine] = end_time
            job_times[job_id] = end_time

            schedule.append({
                'job': job_id, 'operation': op_num, 'machine': machine,
                'start': start_time, 'end': end_time, 'duration': duration
            })
            makespan = max(makespan, end_time)

        return schedule, makespan

    def generate_initial_solution(self):
        operations = []
        for job_id in self.jobs:
            for op_num in range(len(self.jobs[job_id])):
                operations.append((job_id, op_num))
        random.shuffle(operations)
        return operations

    def get_neighbor(self, current_sequence):
        neighbor = current_sequence.copy()
        machine_ops = {}

        for i, (job_id, op_num) in enumerate(neighbor):
            machine = self.jobs[job_id][op_num][0]
            if machine not in machine_ops:
                machine_ops[machine] = []
            machine_ops[machine].append(i)

        valid_machines = [m for m in machine_ops if len(machine_ops[m]) >= 2]
        if not valid_machines:
            return neighbor

        machine = random.choice(valid_machines)
        idx1, idx2 = random.sample(machine_ops[machine], 2)
        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
        return neighbor

    def simulated_annealing(self, initial_temp=1000, cooling_rate=0.99, min_temp=0.01, max_iterations=2000):
        current_solution = self.generate_initial_solution()
        current_schedule, current_makespan = self.decode_schedule(current_solution)
        best_solution = current_solution.copy()
        best_schedule = current_schedule
        best_makespan = current_makespan

        temperature = initial_temp

        print(f"Starting with makespan: {current_makespan}")

        for iteration in range(max_iterations):
            if temperature < min_temp:
                break

            neighbor_solution = self.get_neighbor(current_solution)
            neighbor_schedule, neighbor_makespan = self.decode_schedule(neighbor_solution)
            delta_energy = neighbor_makespan - current_makespan

            if delta_energy < 0:
                current_solution = neighbor_solution
                current_schedule = neighbor_schedule
                current_makespan = neighbor_makespan

                if neighbor_makespan < best_makespan:
                    best_solution = neighbor_solution.copy()
                    best_schedule = neighbor_schedule
                    best_makespan = neighbor_makespan
            else:
                acceptance_prob = math.exp(-delta_energy / temperature)
                if random.random() < acceptance_prob:
                    current_solution = neighbor_solution
                    current_schedule = neighbor_schedule
                    current_makespan = neighbor_makespan

            temperature *= cooling_rate

            if iteration % 200 == 0:
                print(f"Iteration {iteration}: Temperature={temperature:.1f}, Best makespan={best_makespan}")

        print(f"Finished with best makespan: {best_makespan}")
        return best_solution, best_schedule, best_makespan


if __name__ == "__main__":
    jobs = {
        1: [(0, 3), (1, 2), (2, 2)],
        2: [(0, 2), (2, 1), (1, 4)],
        3: [(1, 4), (0, 3), (2, 1)],
    }

    job_shop = JobShopScheduling(jobs)
    best_solution, best_schedule, best_makespan = job_shop.simulated_annealing()

    print("\nBest schedule:")
    for op in best_schedule:
        print(f"Job {op['job']}, Operation {op['operation']}: Machine {op['machine']} from {op['start']} to {op['end']}")