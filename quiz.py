
class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

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
            score -= 2

        elif result == "unanswered":
            score = 0

        if hint_used:
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
        # 데이터가 딕셔너리인지 확인
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

        # 필수 항목 확인
        required_keys = ["question", "choices", "answer"]

        for key in required_keys:
            if key not in data:
                raise ValueError(f"필수 항목이 없습니다: {key}")

        question = data["question"]
        choices = data["choices"]
        answer = data["answer"]
        hint = data.get("hint", "")

        # 자료형 검사
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 내용이 올바르지 않습니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개의 리스트여야 합니다.")

        if not all(isinstance(choice, str) and choice.strip() for choice in choices):
            raise ValueError("선택지 내용이 올바르지 않습니다.")

        if type(answer) is not int or not 1 <= answer <= len(choices):
            raise ValueError("정답 번호가 올바르지 않습니다.")

        if not isinstance(hint, str):
            raise ValueError("힌트 형식이 올바르지 않습니다.")

        return cls(
            question,
            choices,
            answer,
            hint
        )
