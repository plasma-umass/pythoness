from __future__ import annotations

from bs4 import BeautifulSoup
from time import sleep

import json
import leetcode

# Get from browser cookies
SESSION = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTU2MjIxMDEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0YzU1ODI3MmI4MWYyMGI2MTI5MGRjM2M1ODdmNzllYzkxZWYyMWM2N2YzZDI4ODQzNDY1OWRiMDUwNDhmYjJjIiwic2Vzc2lvbl91dWlkIjoiMjEwZjA1NDMiLCJpZCI6MTU2MjIxMDEsImVtYWlsIjoia3lsYS5sZXZpbkBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImtobGV2aW4iLCJ1c2VyX3NsdWciOiJraGxldmluIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2tobGV2aW4vYXZhdGFyXzE3MzE3MjQzMjgucG5nIiwicmVmcmVzaGVkX2F0IjoxNzQxMzY0MTA4LCJpcCI6IjEyOC4xMTkuNDAuMTk2IiwiaWRlbnRpdHkiOiI2ZGJiMTA5NTJhMzhjMTFkMTllMjY0ODAyM2Q1MDU1YiIsImRldmljZV93aXRoX2lwIjpbImFiNGM0Mjg3NGYzMDQzNGEwYmNhM2MxY2UxNTNkNmMyIiwiMTI4LjExOS40MC4xOTYiXX0.tNOvbMpoyc525wO3U9b7PA4d3xcWoaBzC1ZdKrOOqY4"
CSRF = "AgRlMyz6zKAphcqcgSNwf9JDtncqsAoLnCeYFYOYTfbh7WtQueK6lojOkjOaxIQU"


def get_problem_details(name: str) -> dict:

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
        variables=leetcode.GraphqlQueryGetQuestionDetailVariables(title_slug=name),
        operation_name="getQuestionDetail",
    )

    q_details = {}
    try:
        graphql_response = api_instance.graphql_post(body=graphql_request).to_dict()[
            "data"
        ]["question"]

        q_details["name"] = graphql_response["title"]
        q_details["id"] = graphql_response["question_id"]
        q_details["frontend_id"] = graphql_response[
            "question_frontend_id"
        ]  # Not sure how this is different from id

        # Repeat of "code_definition"?
        q_details["template_code_snippet"] = next(
            (
                d
                for d in graphql_response["code_snippets"]
                if d.get("lang") == "Python3"
            ),
            None,
        )["code"]

        # Repeat of "code_snippets"?
        q_details["template_code_definition"] = next(
            (
                d
                for d in json.loads(graphql_response["code_definition"])
                if d.get("value") == "python3"
            ),
            None,
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

    except KeyError as e:
        print("Missing dictionary key: %s\n" % e)
    except json.JSONDecodeError as e:
        print("Failed to parse JSON: %s\n" % e)
    except Exception as e:
        print("An error occurred: %s\n" % e)
    return q_details


def submit_test(name: str, id: int, code: str) -> dict:

    configuration = leetcode.Configuration()

    configuration.api_key["x-csrftoken"] = globals()["CSRF"]
    configuration.api_key["csrftoken"] = globals()["CSRF"]
    configuration.api_key["LEETCODE_SESSION"] = globals()["SESSION"]
    configuration.api_key["Referer"] = "https://leetcode.com"
    configuration.debug = False

    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    # Queue test submission
    test_submission = leetcode.TestSubmission(
        data_input="[1,3]\n[2]",
        typed_code=code,
        question_id=id,
        test_mode=False,
        lang="python3",
    )
    interpretation_id = api_instance.problems_problem_interpret_solution_post(
        problem=name, body=test_submission
    )

    # Wait for sync test result
    while True:
        test_submission_result = api_instance.submissions_detail_id_check_get(
            id=interpretation_id.interpret_id
        )
        if (
            test_submission_result["state"] != "PENDING"
            and test_submission_result["state"] != "STARTED"
        ):
            break
        sleep(1)  # Prevent excessive API calls

    test_submission_result = leetcode.TestSubmissionResult(
        **test_submission_result
    ).to_dict()

    t_details = {}
    try:
        t_details["status_code"] = test_submission_result[
            "status_code"
        ]  # 10 is success, 15 is error
        t_details["run_success"] = test_submission_result["run_success"]  # T/F
        t_details["runtime_error"] = test_submission_result["runtime_error"]
        t_details["full_runtime_error"] = test_submission_result["full_runtime_error"]
        t_details["answer"] = test_submission_result["code_answer"]
        t_details["output"] = test_submission_result["code_output"]
        t_details["elapsed_time"] = test_submission_result["elapsed_time"]  # Unit?
        t_details["memory"] = test_submission_result["memory"]  # Unit?
        t_details["task_finish_time"] = test_submission_result[
            "task_finish_time"
        ]  # Unit?
        t_details["expected_answer"] = test_submission_result["expected_code_answer"]
        t_details["expected_output"] = test_submission_result["expected_code_output"]
        t_details["correct_answer"] = test_submission_result[
            "correct_answer"
        ]  # true, false
        t_details["status_msg"] = test_submission_result[
            "status_msg"
        ]  # Accepted, Wrong Answer, Runtime Error
        t_details["state"] = test_submission_result["state"]  # SUCCESS
    except KeyError as e:
        print("Missing dictionary key: %s\n" % e)
    except Exception as e:
        print("An error occurred: %s\n" % e)

    return


def submit_solution(name: str, id: int, code: str) -> dict:
    configuration = leetcode.Configuration()

    configuration.api_key["x-csrftoken"] = globals()["CSRF"]
    configuration.api_key["csrftoken"] = globals()["CSRF"]
    configuration.api_key["LEETCODE_SESSION"] = globals()["SESSION"]
    configuration.api_key["Referer"] = "https://leetcode.com"
    configuration.debug = False

    api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

    # Queue real submission
    submission = leetcode.Submission(
        judge_type="large",
        typed_code=code,
        question_id=id,
        test_mode=False,
        lang="python3",
    )
    submission_id = api_instance.problems_problem_submit_post(
        problem=name, body=submission
    )

    # Wait for sync submission result
    while True:
        submission_result = api_instance.submissions_detail_id_check_get(
            id=submission_id.submission_id
        )
        if (
            submission_result["state"] != "PENDING"
            and submission_result["state"] != "STARTED"
        ):
            break
        sleep(1)  # Prevent excessive API calls

    submission_response = leetcode.SubmissionResult(**submission_result).to_dict()

    s_details = {}
    try:
        s_details["state"] = submission_response["state"]  # SUCCESS
        s_details["status_code"] = submission_response[
            "status_code"
        ]  # 10 is success, 15 is error
        s_details["run_success"] = submission_response["run_success"]  # T/F
        s_details["status_msg"] = submission_response[
            "status_msg"
        ]  # Accepted, Wrong Answer, Runtime Error
        s_details["runtime_error"] = submission_response["runtime_error"]
        s_details["full_runtime_error"] = submission_response["full_runtime_error"]
        s_details["std_output"] = submission_response["std_output"]
        s_details["elapsed_time"] = submission_response["elapsed_time"]  # Unit?
        s_details["memory"] = submission_response["memory"]  # Unit?
        s_details["correct_testcases"] = submission_response["total_correct"]
        s_details["num_testcases"] = submission_response["total_testcases"]

        # Info for the last failing testcase
        s_details["input"] = submission_response["input"]
        s_details["input_formatted"] = submission_response["input_formatted"]
        s_details["last_testcase_input"] = submission_response[
            "last_testcase"
        ]  # Same as "input"?
        s_details["output"] = submission_response["code_output"]
        s_details["last_testcase_output"] = submission_response["expected_output"]

        # Solution stats if all test cases passed
        s_details["memory_percentile"] = submission_response["memory_percentile"]
        s_details["runtime_percentile"] = submission_response["runtime_percentile"]
    except KeyError as e:
        print("Missing dictionary key: %s\n" % e)
    except Exception as e:
        print("An error occurred: %s\n" % e)

    return s_details
