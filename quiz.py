
class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer

    def show_question(self):
        print(self.question)

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def evaluate_answer(self, user_answer):
        if user_answer is None:
            return "unanswered"
        if self.answer == user_answer:
            return "correct"
        else:
            return "incorrect"

    def show_hint(self):
        if self.hint:
            print(f"힌트: {self.hint}")
        else:
            print("등록된 힌트가 없습니다.")

    def show_answer(self):
        print(f"정답은 {self.answer}번입니다.")
        print(f"정답 내용: {self.choices[self.answer - 1]}")

    def calculate_score(self, result, hint_used):
        score = 0
        if result == "correct":
            score = 5

        elif result == "incorrect":
            score = 0

        elif result == "unanswered":
            score = 0

        if hint_used:
            score -= 2

        if result == "incorrect":
            score -= 2

        return score

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["question"],
            data["choices"],
            data["answer"]
            data.get("hint", "")
        )
