"""
Hash table with separate chaining (list per bucket), keyed on city_id.

Went with chaining over open addressing mainly because city_id in this
dataset is dense-ish but has gaps here and there, and linear probing
tends to clump up (primary clustering) when keys aren't perfectly
uniform. Chaining just degrades to a slightly longer list per bucket
instead of causing probe pileups everywhere.

Resizes (doubles capacity) once load factor goes over 0.75 so it doesn't
slowly turn into a glorified linked list as more cities get added.
"""

class HashTable:
    def __init__(self, capacity=16):
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def __len__(self):
        return self._size

    def _hash(self, city_id):
        return hash(city_id) % self._capacity

    def _maybe_resize(self):
        if self._size / self._capacity > 0.75:
            old_buckets = self._buckets
            self._capacity *= 2
            self._buckets = [[] for _ in range(self._capacity)]
            self._size = 0
            for bucket in old_buckets:
                for city in bucket:
                    self.insert(city)  # re-insert everything into the bigger table

    def insert(self, city):
        idx = self._hash(city.city_id)
        bucket = self._buckets[idx]
        for i, c in enumerate(bucket):
            if c.city_id == city.city_id:
                bucket[i] = city  # id already exists, overwrite it
                return
        bucket.append(city)
        self._size += 1
        self._maybe_resize()

    def search(self, city_id):
        idx = self._hash(city_id)
        for c in self._buckets[idx]:
            if c.city_id == city_id:
                return c
        return None

    def delete(self, city_id):
        idx = self._hash(city_id)
        bucket = self._buckets[idx]
        for i, c in enumerate(bucket):
            if c.city_id == city_id:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def load_factor(self):
        return self._size / self._capacity
    