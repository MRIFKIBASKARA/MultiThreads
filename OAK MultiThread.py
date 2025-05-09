import threading
import time
import random

# Simulasi memory utama
main_memory = {"x": 0}
lock = threading.Lock()

# Statistik
cache_traffic = {"with_coherence": 0, "without_coherence": 0}
message_logs = []

# Konfigurasi
NUM_THREADS = 4
NUM_ACCESSES = 100

# Cache dengan koherensi (sederhana)
class CoherentCache:
    def __init__(self):
        self.local_cache = {}
    
    def read(self, key):
        with lock:
            cache_traffic["with_coherence"] += 1
            self.local_cache[key] = main_memory[key]
            message_logs.append(f"READ {key} from main memory")
        return self.local_cache[key]

    def write(self, key, value):
        with lock:
            cache_traffic["with_coherence"] += 1
            main_memory[key] = value
            message_logs.append(f"WRITE {key} to main memory")
            # Invalidate all other caches (sederhana, simulasi saja)
            self.local_cache[key] = value

# Cache tanpa koherensi
class NonCoherentCache:
    def __init__(self):
        self.local_cache = {"x": 0}
    
    def read(self, key):
        cache_traffic["without_coherence"] += 1
        return self.local_cache[key]

    def write(self, key, value):
        cache_traffic["without_coherence"] += 1
        self.local_cache[key] = value

def simulate_access(cache_type, coherence_enabled):
    for _ in range(NUM_ACCESSES):
        key = "x"
        if coherence_enabled:
            value = cache_type.read(key)
            new_value = value + 1
            cache_type.write(key, new_value)
        else:
            value = cache_type.read(key)
            new_value = value + 1
            cache_type.write(key, new_value)

def run_simulation(coherence_enabled):
    threads = []
    for _ in range(NUM_THREADS):
        cache = CoherentCache() if coherence_enabled else NonCoherentCache()
        t = threading.Thread(target=simulate_access, args=(cache, coherence_enabled))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# Jalankan simulasi
print("⏱️ Simulasi dengan KOHERENSI:")
run_simulation(coherence_enabled=True)
print("Traffic dengan koherensi:", cache_traffic["with_coherence"])
print("Memori akhir (x):", main_memory["x"])
print()

# Reset untuk simulasi tanpa koherensi
main_memory["x"] = 0
print("⏱️ Simulasi TANPA koherensi:")
run_simulation(coherence_enabled=False)
print("Traffic tanpa koherensi:", cache_traffic["without_coherence"])
print("Memori akhir (x):", main_memory["x"])
