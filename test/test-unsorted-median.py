import pythoness

@pythoness.spec("""Given an unsorted list of integers l, find the median of l. If the list
                is empty, return None.""",
                tests=["find_median([1,5,7,4,3]) == 4",
                       "find_median([100,94,39,19,20,75,3]) == 39"])

def find_median(l : list):
    ""

print("Running tests: unsorted-median")
assert(find_median([4,-3,5]) == 4)
assert(find_median([5,2,1,9]) == 3.5)
assert(find_median([3]) == 3)
assert(find_median([]) == None)
print("Tests complete.")
