import bisect


# XXX NOT USED
class Node:

    def __init__(self, key, value):
        self.key = key
        self.values = [value]
        self.left = None
        self.right = None
        self.scores = []

    def __contains__(self, value):
        if value in self.value:
            return True
        if value in self.left:
            return True
        if value in self.right:
            return True
        return False

    def popval(self, value):
        pass

    def insert(self, key, value):
        if key < self.key:
            if self.left is None:
                self.left = Node(key, value)
            else:
                self.left.insert(key, value)
        elif key == self.key:
            new_values = []
            inserted = False
            for v in self.values:
                if value < v and not inserted:
                    new_values.append(value)
                    inserted = True
                new_values.append(v)
        if key > self.key:
            if self.right is None:
                self.right = Node(key, value)
            else:
                self.right.insert(key, value)

    def rem(value):
        pass


class SortedSet:

    def __init__(self):
        self.key_to_value = {}
        self.value_to_key = {}
        self.ranked_keys = []
        self.cardinality = 0

    def __repr__(self):
        return "k->v: {}\nv->k: {}\nrank: {}".format(self.key_to_value,
                                                     self.value_to_key, self.ranked_keys)

    def insert(self, key, value):
        key = int(key)
        self.remove(value)

        self.key_to_value[key] = value
        self.value_to_key[value] = key
        bisect.insort(self.ranked_keys, key)
        self.cardinality += 1

    def remove(self, value):
        if value in self.value_to_key:
            key = self.value_to_key.pop(value)
            self.key_to_value.pop(key)
            rank = bisect.bisect_left(self.ranked_keys, key)
            del self.ranked_keys[rank]
            self.cardinality -= 1

    def count(self, min_rank, max_rank):
        left = bisect.bisect_left(self.ranked_keys, min_rank)
        right = bisect.bisect_right(self.ranked_keys, max_rank)
        return right - left

    def rank(self, value):
        if value in self.value_to_key:
            key = self.value_to_key[value]
            return bisect.bisect_left(self.ranked_keys, key)
        return None

    def range(self, min_value, max_value, with_scores=None):
        left = bisect.bisect_left(self.ranked_keys, min_value)
        right = bisect.bisect_right(self.ranked_keys, max_value)
        print(left, right, self.ranked_keys)
        scores = self.ranked_keys[left:right+1]
        return [self.key_to_value[x] for x in scores]
