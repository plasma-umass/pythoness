import pythoness


@pythoness.spec(
    "Concatenates three lists, l1, l2, l3",
    tests=[
        (
            {"l1": "lists(text())", "l2": "lists(text())", "l3": "lists(text())"},
            "len(l1) + len(l2) + len(l3) == len(triconcat(l1, l2, l3))",
        )
    ],
)
def triconcat(l1: list, l2: list, l3: list) -> list:
    """"""


print("Running tests: triconcat")
assert triconcat(["a"], ["b"], ["c", "d"]) == ["a", "b", "c", "d"]
print("Tests complete.")
