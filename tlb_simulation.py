import random
from collections import deque, defaultdict

# -----------------------------
# Process / Workload Generator
# -----------------------------
def generate_workload(num_accesses=1000, working_set_size=10, address_space=1000, locality_strength=0.9):
    """
    Generates memory accesses with locality.
    locality_strength: probability of staying in working set
    """
    working_set = random.sample(range(address_space), working_set_size)
    accesses = []

    for _ in range(num_accesses):
        if random.random() < locality_strength:
            accesses.append(random.choice(working_set))
        else:
            accesses.append(random.randint(0, address_space - 1))

    return accesses


# -----------------------------
# TLB Implementation
# -----------------------------
class TLB:
    def __init__(self, size, algorithm="LRU"):
        self.size = size
        self.algorithm = algorithm
        self.cache = []
        self.queue = deque()  # for FIFO
        self.freq = defaultdict(int)  # for LFU (optional)

    def access(self, address):
        # HIT
        if address in self.cache:
            if self.algorithm == "LRU":
                self.cache.remove(address)
                self.cache.append(address)
            return True

        # MISS
        if len(self.cache) >= self.size:
            self.evict()

        self.cache.append(address)

        if self.algorithm == "FIFO":
            self.queue.append(address)

        return False

    def evict(self):
        if self.algorithm == "LRU":
            self.cache.pop(0)

        elif self.algorithm == "FIFO":
            oldest = self.queue.popleft()
            self.cache.remove(oldest)

        elif self.algorithm == "Random":
            victim = random.choice(self.cache)
            self.cache.remove(victim)


# -----------------------------
# Simulation Runner
# -----------------------------
def run_simulation(accesses, tlb_size, algorithm, hit_time=1, miss_time=20):
    tlb = TLB(tlb_size, algorithm)

    hits = 0
    total_time = 0

    for addr in accesses:
        if tlb.access(addr):
            hits += 1
            total_time += hit_time
        else:
            total_time += miss_time

    total_accesses = len(accesses)
    hit_rate = hits / total_accesses
    miss_rate = 1 - hit_rate
    avg_time = total_time / total_accesses

    return {
        "hit_rate": hit_rate,
        "miss_rate": miss_rate,
        "avg_time": avg_time
    }


# -----------------------------
# Experiment Framework
# -----------------------------
def run_experiments():
    algorithms = ["LRU", "FIFO", "Random"]
    tlb_sizes = [4, 8, 16, 32]

    print("\n=== TLB Simulation Results ===\n")
    print(f"{'Algo':<10}{'Size':<6}{'Hit Rate':<10}{'Avg Time':<10}")

    for size in tlb_sizes:
        # Generate workload (you can tweak parameters)
        accesses = generate_workload(
            num_accesses=2000,
            working_set_size=10,
            locality_strength=0.9
        )

        for algo in algorithms:
            result = run_simulation(accesses, size, algo)

            print(f"{algo:<10}{size:<6}{result['hit_rate']:<10.3f}{result['avg_time']:<10.2f}")


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    run_experiments()