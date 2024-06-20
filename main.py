import sys
import json
import typing


# TYPES
class Question(typing.TypedDict):
    text: str
    options: list[str]
    answer: int


class Quiz(typing.TypedDict):
    title: str
    description: str
    questions: list[Question]


class Record(typing.TypedDict):
    question: Question
    your_answer: int


# FUNTIONS
def load_quiz(filename: str) -> Quiz:
    """This function loads a quiz from a json file.
    filename is the name of the json file
    """
    try:
        with open(filename) as file:
            return json.load(file)
    except FileNotFoundError:
        sys.exit("File not found")
    except json.JSONDecodeError:
        sys.exit("Invalid json file")


def line():
    print("+---------------------------------------")


def ask_question(index: int, question: Question) -> int:
    """This asks a single question"""

    try:
        text = question["text"]
        options = question["options"]
        answer = question["answer"]
    except KeyError:
        sys.exit(f"Invalid question format at question {index}")

    print(f"Q{index}: {text}")

    for option_index, option in enumerate(options):
        print(f"\t{option_index}) {option}")

    try:
        user_answer = input("")
    except KeyboardInterrupt:
        sys.exit("You quit the quiz")

    user_answer = int(user_answer)

    line()

    return user_answer


def print_quiz_intro(quiz: Quiz):
    try:
        title = quiz["title"]
        description = quiz["description"]
        quiz["questions"]
    except KeyError:
        sys.exit("Invalid question format")

    line()
    print(title.upper())
    print(description)
    line()


def main():
    if len(sys.argv) < 2:
        sys.exit("Pass a json file")

    json_file = sys.argv[1]
    print("Opening json file:", json_file)

    quiz = load_quiz(json_file)
    print_quiz_intro(quiz)
    questions = quiz["questions"]

    record_list: list[Record] = []

    for index, question in enumerate(questions):
        user_answer = ask_question(index, question)
        record: Record = {"question": question, "your_answer": user_answer}
        record_list.append(record)

    line()

    score = 0

    for index, record in enumerate(record_list):
        question = record["question"]
        print(f"Q{index}: {question['text']}")
        print(f"Your answer: {question['options'][record['your_answer']]}")
        print(f"Correct answer: {question['options'][question['answer']]}")

        if question["answer"] == record["your_answer"]:
            score += 1

        line()

    percentage_score = (score / len(questions)) * 100
    print(f"You scored: {percentage_score}%")


main()
