from __future__ import annotations

from bs4 import BeautifulSoup
from time import sleep

import json
import leetcode
import pprint

# Get from browser cookies
SESSION = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTU2MjIxMDEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0YzU1ODI3MmI4MWYyMGI2MTI5MGRjM2M1ODdmNzllYzkxZWYyMWM2N2YzZDI4ODQzNDY1OWRiMDUwNDhmYjJjIiwic2Vzc2lvbl91dWlkIjoiMjEwZjA1NDMiLCJpZCI6MTU2MjIxMDEsImVtYWlsIjoia3lsYS5sZXZpbkBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImtobGV2aW4iLCJ1c2VyX3NsdWciOiJraGxldmluIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2tobGV2aW4vYXZhdGFyXzE3MzE3MjQzMjgucG5nIiwicmVmcmVzaGVkX2F0IjoxNzQxMzY0MTA4LCJpcCI6IjEyOC4xMTkuNDAuMTk2IiwiaWRlbnRpdHkiOiI2ZGJiMTA5NTJhMzhjMTFkMTllMjY0ODAyM2Q1MDU1YiIsImRldmljZV93aXRoX2lwIjpbImFiNGM0Mjg3NGYzMDQzNGEwYmNhM2MxY2UxNTNkNmMyIiwiMTI4LjExOS40MC4xOTYiXX0.tNOvbMpoyc525wO3U9b7PA4d3xcWoaBzC1ZdKrOOqY4"
CSRF = "AgRlMyz6zKAphcqcgSNwf9JDtncqsAoLnCeYFYOYTfbh7WtQueK6lojOkjOaxIQU"


def _get_problem_details():

    configuration = leetcode.Configuration()

    configuration.api_key["x-csrftoken"] = globals()["CSRF"]
    configuration.api_key["csrftoken"] = globals()["CSRF"]
    configuration.api_key["LEETCODE_SESSION"] = globals()["SESSION"]
    configuration.api_key["Referer"] = "https://leetcode.com"
    configuration.debug = False

    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    graphql_request = leetcode.GraphqlQuery(
        query="""
            query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                questionFrontendId
                boundTopicId
                title
                content
                translatedTitle
                isPaidOnly
                difficulty
                likes
                dislikes
                isLiked
                similarQuestions
                contributors {
                username
                profileUrl
                avatarUrl
                __typename
                }
                langToValidPlayground
                topicTags {
                name
                slug
                translatedName
                __typename
                }
                companyTagStats
                codeSnippets {
                lang
                langSlug
                code
                __typename
                }
                stats
                codeDefinition
                hints
                solution {
                id
                canSeeDetail
                __typename
                }
                status
                sampleTestCase
                enableRunCode
                metaData
                translatedContent
                judgerAvailable
                judgeType
                mysqlSchemas
                enableTestMode
                envInfo
                __typename
            }
            }
        """,
        variables=leetcode.GraphqlQueryGetQuestionDetailVariables(
            title_slug="median-of-two-sorted-arrays"
        ),
        operation_name="getQuestionDetail",
    )

    graphql_response = api_instance.graphql_post(body=graphql_request).to_dict()[
        "data"
    ]["question"]

    with open("clean_1_raw.json", "w") as json_file:
        json.dump(graphql_response, json_file, indent=4)

    q_details = {}
    q_details["name"] = graphql_response["title"]
    q_details["id"] = graphql_response["question_id"]
    q_details["frontend_id"] = graphql_response[
        "question_frontend_id"
    ]  # Not sure how this is different

    # Repeat of "code_definition"?
    q_details["template_code_snippet"] = next(
        (d for d in graphql_response["code_snippets"] if d.get("lang") == "Python3"),
        None,
    )["code"]

    # Repeat of "code_snippets"?
    description = graphql_response["code_definition"]  # Str of JSON
    try:
        description = json.loads(description)  # Convert to dict
    except json.JSONDecodeError as e:
        print("Parsing failed:", e)
    # Filter dict for only python3 version, None if not found
    q_details["template_code_definition"] = next(
        (d for d in description if d.get("value") == "python3"), None
    )["defaultCode"]

    q_details["problem_statement"] = BeautifulSoup(
        graphql_response["content"].replace("<sup>", "^").replace("</sup>", ""),
        "html.parser",
    ).get_text()

    q_details["difficulty"] = graphql_response["difficulty"]
    q_details["premium"] = graphql_response["is_paid_only"]

    q_details["enable_run_code"] = graphql_response["enable_run_code"]  # True
    q_details["enable_test_mode"] = graphql_response["enable_test_mode"]  # False

    # Idk what the judge is
    q_details["judge_type"] = graphql_response["judge_type"]  # 'Small'
    q_details["judger_available"] = graphql_response["judger_available"]  # True

    q_details["sample_test_case"] = graphql_response[
        "sample_test_case"
    ]  # Input args for sample

    with open("clean_1.json", "w") as json_file:
        json.dump(graphql_response, json_file, indent=4)

    return q_details


def _submit_test(code):

    configuration = leetcode.Configuration()

    configuration.api_key["x-csrftoken"] = globals()["CSRF"]
    configuration.api_key["csrftoken"] = globals()["CSRF"]
    configuration.api_key["LEETCODE_SESSION"] = globals()["SESSION"]
    configuration.api_key["Referer"] = "https://leetcode.com"
    configuration.debug = False

    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    test_submission = leetcode.TestSubmission(
        data_input="[2,7,11,15]\n9",
        typed_code=code,
        question_id=1,
        test_mode=False,
        lang="python",
    )

    interpretation_id = api_instance.problems_problem_interpret_solution_post(
        problem="two-sum", body=test_submission
    )

    print("Test has been queued. Result:")
    print(interpretation_id)

    while True:
        test_submission_result = api_instance.submissions_detail_id_check_get(
            id=interpretation_id.interpret_id
        )

        if test_submission_result["state"] != "PENDING":
            break

        sleep(1)  # Prevent excessive API calls

    print("Got test result:")
    print(test_submission_result)

    print(leetcode.TestSubmissionResult(**test_submission_result))

    return


def _submit_solution(code):
    configuration = leetcode.Configuration()

    configuration.api_key["x-csrftoken"] = globals()["CSRF"]
    configuration.api_key["csrftoken"] = globals()["CSRF"]
    configuration.api_key["LEETCODE_SESSION"] = globals()["SESSION"]
    configuration.api_key["Referer"] = "https://leetcode.com"
    configuration.debug = False

    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    # Real submission
    submission = leetcode.Submission(
        judge_type="large",
        typed_code=code,
        question_id=1,
        test_mode=False,
        lang="python",
    )

    submission_id = api_instance.problems_problem_submit_post(
        problem="two-sum", body=submission
    )

    print("Submission has been queued. Result:")
    print(submission_id)

    while True:
        submission_result = api_instance.submissions_detail_id_check_get(
            id=submission_id.submission_id
        )

        if submission_result["state"] != "PENDING":
            break

        sleep(1)  # Prevent excessive API calls

    print("Got submission result:")
    print(leetcode.SubmissionResult(**submission_result))


def run():
    # problem_details = _get_problem_details()
    problem_details = {}
    with open("clean_1.json", "r") as json_file:
        problem_details = json.load(json_file)

    solution_code = """
    class Solution:
        def twoSum(self, nums, target):
            print("stdout")
            return [1]
    """

    submission = _submit_test(solution_code)
    submission = _submit_solution(solution_code)
    return


if __name__ == "__main__":
    run()
