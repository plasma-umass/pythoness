import requests


def get_hard_leetcode_problems():
    url = "https://leetcode.com/api/problems/all/"
    response = requests.get(url)

    if response.status_code != 200:
        print("Failed to fetch problems.")
        return

    data = response.json()
    problems = data.get("stat_status_pairs", [])

    hard_problems = [
        (problem["stat"]["frontend_question_id"], problem["stat"]["question__title"])
        for problem in problems
        if problem.get("difficulty", {}).get("level") == 3
    ]

    for number, title in sorted(hard_problems):
        print(f"{number}: {title}")


if __name__ == "__main__":
    get_hard_leetcode_problems()
