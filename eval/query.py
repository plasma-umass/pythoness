from __future__ import annotations

from bs4 import BeautifulSoup
from time import sleep

import json
import leetcode
import unicodedata

# Get from browser cookies
# SESSION = ""
SESSION = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTU2MjIxMDEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJhbGxhdXRoLmFjY291bnQuYXV0aF9iYWNrZW5kcy5BdXRoZW50aWNhdGlvbkJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0YzU1ODI3MmI4MWYyMGI2MTI5MGRjM2M1ODdmNzllYzkxZWYyMWM2N2YzZDI4ODQzNDY1OWRiMDUwNDhmYjJjIiwic2Vzc2lvbl91dWlkIjoiNTk5ZDkwYWMiLCJpZCI6MTU2MjIxMDEsImVtYWlsIjoia3lsYS5sZXZpbkBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImtobGV2aW4iLCJ1c2VyX3NsdWciOiJraGxldmluIiwiYXZhdGFyIjoiaHR0cHM6Ly9hc3NldHMubGVldGNvZGUuY29tL3VzZXJzL2tobGV2aW4vYXZhdGFyXzE3MzE3MjQzMjgucG5nIiwicmVmcmVzaGVkX2F0IjoxNzQxODE1NTI3LCJpcCI6IjEyOC4xMTkuNDAuMTk2IiwiaWRlbnRpdHkiOiIzZmEzMWI1MmRkNmViYzUxN2U1NDkyZDQzZDc3ZTYxYyIsImRldmljZV93aXRoX2lwIjpbIjljZTIyMWNlOGZmZTQ5MDRkZTI0NTQ5NmRjOWQyMzdjIiwiMTI4LjExOS40MC4xOTYiXX0.hVNK5uuSlQ2S4ZrwJmTKty2Zfkv5QqI6AEO01H_PUAA"
CSRF = "dmgrYkogyPzOaonX18fJ557gEF9SwwKcKu0vIVUP5osKHzRUpk00miKXg5d8vJoR"


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

        unicode_statement = BeautifulSoup(
            graphql_response["content"].replace("<sup>", "^").replace("</sup>", ""),
            "html.parser",
        ).get_text()
        unicode_statement = unicodedata.normalize("NFKD", unicode_statement)
        q_details["problem_statement"] = unicode_statement.replace("\xa0", " ").replace(
            "\u200b", " "
        )

        q_details["difficulty"] = graphql_response["difficulty"]
        q_details["premium"] = graphql_response["is_paid_only"]

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
