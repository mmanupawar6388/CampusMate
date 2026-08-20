VIVA_BANK = {
    "Python": [
        {
            "question": "What is the difference between a list and a tuple in Python?",
            "concepts": {
                "list": ["list", "square brackets"],
                "tuple": ["tuple", "parentheses", "round brackets"],
                "mutable": ["mutable", "can be changed", "can change", "can be modified", "changeable"],
                "immutable": ["immutable", "cannot be changed", "can't be changed", "cannot be modified", "can't be modified", "unchangeable"]
            },
            "answer": "A list is mutable, so its elements can be changed after creation. A tuple is immutable, so its elements cannot be changed after creation."
        },
        {
            "question": "What is object-oriented programming?",
            "concepts": {
                "object": ["object", "objects"],
                "class": ["class", "classes"],
                "encapsulation": ["encapsulation", "data hiding"],
                "inheritance": ["inheritance", "reusability", "reuse"],
                "polymorphism": ["polymorphism", "many forms"]
            },
            "answer": "Object-oriented programming is a programming approach based on objects and classes. Important concepts include encapsulation, inheritance, polymorphism and abstraction."
        },
        {
            "question": "What is exception handling in Python?",
            "concepts": {
                "exception": ["exception", "error"],
                "try": ["try"],
                "except": ["except"],
                "finally": ["finally"]
            },
            "answer": "Exception handling allows a program to handle runtime errors without crashing. Python commonly uses try, except, else and finally blocks."
        },
        {
            "question": "What is the difference between == and is in Python?",
            "concepts": {
                "value": ["value", "values"],
                "identity": ["identity", "same object"],
                "equal": ["equal", "equality"]
            },
            "answer": "== compares values, while is checks whether two references point to the same object."
        },
        {
            "question": "What is inheritance?",
            "concepts": {
                "class": ["class", "classes"],
                "parent": ["parent", "base class"],
                "child": ["child", "derived class"],
                "reuse": ["reuse", "reusability", "inherit"]
            },
            "answer": "Inheritance allows a child class to acquire attributes and methods from a parent class, supporting code reuse and hierarchical design."
        }
    ],

    "Machine Learning": [
        {
            "question": "What is supervised learning?",
            "concepts": {
                "labeled": ["labeled", "labelled"],
                "data": ["data", "dataset"],
                "input": ["input", "inputs"],
                "output": ["output", "outputs", "target"],
                "prediction": ["prediction", "predict"]
            },
            "answer": "Supervised learning trains a model using labeled data, where the input and expected output are known."
        },
        {
            "question": "What is overfitting?",
            "concepts": {
                "training": ["training", "train"],
                "unseen": ["unseen", "new data", "test data"],
                "generalize": ["generalize", "generalization"],
                "noise": ["noise"]
            },
            "answer": "Overfitting occurs when a model learns the training data too closely, including noise, and performs poorly on unseen data."
        },
        {
            "question": "What is underfitting?",
            "concepts": {
                "simple": ["simple", "too simple"],
                "pattern": ["pattern", "patterns"],
                "training": ["training", "train"],
                "poor": ["poor", "poorly"]
            },
            "answer": "Underfitting occurs when a model is too simple to capture important patterns in the data, causing poor performance even on training data."
        }
    ],

    "DBMS": [
        {
            "question": "What is a primary key?",
            "concepts": {
                "unique": ["unique", "uniquely"],
                "identify": ["identify", "identifies"],
                "record": ["record", "row"]
            },
            "answer": "A primary key uniquely identifies each record in a table."
        },
        {
            "question": "What is normalization?",
            "concepts": {
                "redundancy": ["redundancy", "duplicate data", "duplication"],
                "tables": ["tables", "table"],
                "anomalies": ["anomalies", "update anomalies"]
            },
            "answer": "Normalization organizes database tables to reduce unnecessary data redundancy and update anomalies."
        }
    ],

    "Computer Networks": [
        {
            "question": "What is an IP address?",
            "concepts": {
                "address": ["address", "ip address"],
                "device": ["device", "host"],
                "network": ["network"],
                "identify": ["identify", "identifies"]
            },
            "answer": "An IP address is a numerical address used to identify a device or network interface on a network."
        },
        {
            "question": "What is DNS?",
            "concepts": {
                "domain": ["domain", "domain name"],
                "ip": ["ip", "ip address"],
                "resolve": ["resolve", "translates", "translation"]
            },
            "answer": "DNS translates human-readable domain names into IP addresses."
        }
    ],

    "Data Structures": [
        {
            "question": "What is a stack?",
            "concepts": {
                "LIFO": ["lifo", "last in first out"],
                "push": ["push"],
                "pop": ["pop"]
            },
            "answer": "A stack is a linear data structure that follows LIFO: Last In, First Out. Common operations are push and pop."
        },
        {
            "question": "What is a queue?",
            "concepts": {
                "FIFO": ["fifo", "first in first out"],
                "enqueue": ["enqueue"],
                "dequeue": ["dequeue"]
            },
            "answer": "A queue is a linear data structure that follows FIFO: First In, First Out. Common operations are enqueue and dequeue."
        }
    ],
}


def get_topics():
    return list(VIVA_BANK.keys())


def start_viva(topic):
    if topic not in VIVA_BANK:
        return None, "Choose a valid topic."

    return 0, VIVA_BANK[topic][0]["question"]


def evaluate_answer(topic, question_index, user_answer):
    questions = VIVA_BANK.get(topic)

    if not questions:
        return "Invalid topic.", question_index, ""

    if not user_answer.strip():
        return "Please enter your answer first.", question_index, ""

    item = questions[question_index]
    answer = user_answer.lower()

    matched = []
    missing = []

    for concept, phrases in item["concepts"].items():
        found = any(
            phrase.lower() in answer
            for phrase in phrases
        )

        if found:
            matched.append(concept)
        else:
            missing.append(concept)

    total_concepts = len(item["concepts"])

    concept_score = (
        len(matched) / total_concepts
        if total_concepts
        else 0
    )

    # Strong answers should be rewarded for communicating the
    # meaning even when they do not use textbook terminology.
    final_score = round(concept_score * 10)

    if final_score >= 8:
        verdict = "Excellent"
    elif final_score >= 6:
        verdict = "Good"
    elif final_score >= 4:
        verdict = "Needs improvement"
    else:
        verdict = "Weak"

    feedback = (
        f"### Score: {final_score}/10\n\n"
        f"**Verdict:** {verdict}\n\n"
        f"**Concept coverage:** {round(concept_score * 100)}%\n\n"
        f"**Matched concepts:** "
        f"{', '.join(matched) if matched else 'None'}\n\n"
        f"**Possible missing concepts:** "
        f"{', '.join(missing) if missing else 'None'}\n\n"
        f"**Better viva answer:**\n"
        f"{item['answer']}"
    )

    return feedback, question_index, item["question"]
