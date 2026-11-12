
import json
import random

from datetime import datetime
from pathlib import Path

from quiz import Quiz


class QuizGame:
    """
    퀴즈 게임의 전체 기능을 관리하는 클래스
    """

    def __init__(self, default_quizzes):
        # 기본 퀴즈 목록
        self.default_quizzes = default_quizzes

        # 실제 게임에서 사용할 퀴즈 목록
        self.quizzes = []

        # 최고 점수
        self.best_score = 0

        # 게임 기록
        self.history = []

        # JSON 파일 경로
        self.state_file = Path(__file__).resolve().parent / "state.json"

        # 저장된 데이터 불러오기
        self.load_state()

    # ---------------------------------
    # 1. 데이터 불러오기
    # ---------------------------------

    def load_state(self):
        """
        state.json 파일에서 퀴즈, 최고 점수, 기록을 불러온다.
        파일이 없거나 손상되었다면 기본 데이터를 사용한다.
        """

        if not self.state_file.exists():
            print("저장된 데이터가 없습니다. 기본 퀴즈를 사용합니다.")
            self.quizzes = self.default_quizzes.copy()
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # JSON의 기본 구조 확인
            if not isinstance(data, dict):
                raise ValueError("저장 데이터 형식이 올바르지 않습니다.")

            quiz_data = data.get("quizzes")
            best_score = data.get("best_score", 0)
            history = data.get("history", [])

            if not isinstance(quiz_data, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

            if not isinstance(best_score, (int, float)):
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")

            if not isinstance(history, list):
                raise ValueError("게임 기록 형식이 올바르지 않습니다.")

            # JSON 데이터를 Quiz 객체로 변환
            loaded_quizzes = []

            for item in quiz_data:
                loaded_quizzes.append(Quiz.from_dict(item))

            self.quizzes = loaded_quizzes
            self.best_score = best_score
            self.history = history

            print("저장된 데이터를 불러왔습니다.")

        except (json.JSONDecodeError, ValueError, TypeError, KeyError) as error:
            print(f"저장 데이터에 문제가 있습니다: {error}")
            print("기본 퀴즈 데이터로 초기화합니다.")

            self.quizzes = self.default_quizzes.copy()
            self.best_score = 0
            self.history = []

            self.save_state()

        except OSError as error:
            print(f"파일을 읽을 수 없습니다: {error}")
            print("기본 퀴즈 데이터로 게임을 시작합니다.")

            self.quizzes = self.default_quizzes.copy()
            self.best_score = 0
            self.history = []

    # ---------------------------------
    # 2. 데이터 저장하기
    # ---------------------------------

    def save_state(self):
        """
        현재 퀴즈, 최고 점수, 게임 기록을
        state.json 파일에 저장한다.
        """

        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history
        }

        try:
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except OSError as error:
            print(f"데이터 저장에 실패했습니다: {error}")

    # ---------------------------------
    # 3. 입력값 검증
    # ---------------------------------

    def get_valid_number(self, message, min_value, max_value):
        """
        숫자를 입력받고 지정된 범위에 해당하는지 확인한다.
        """

        while True:
            user_input = input(message).strip()

            if user_input == "":
                print("빈 값은 입력할 수 없습니다.")
                continue

            try:
                number = int(user_input)

                if min_value <= number <= max_value:
                    return number

                print(
                    f"{min_value}부터 {max_value} 사이의 숫자를 입력하세요."
                )

            except ValueError:
                print("숫자만 입력할 수 있습니다.")

    def get_valid_text(self, message):
        """
        빈 문자열이 입력되지 않도록 검사한다.
        """

        while True:
            user_input = input(message).strip()

            if user_input:
                return user_input

            print("빈 내용은 입력할 수 없습니다.")

    # ---------------------------------
    # 4. 메인 메뉴
    # ---------------------------------

    def show_menu(self):
        """
        프로그램의 메인 메뉴를 출력한다.
        """

        print("\n========== Python Quiz Game ==========")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 점수 기록 확인")
        print("7. 프로그램 종료")
        print("======================================")

    # ---------------------------------
    # 5. 프로그램 실행
    # ---------------------------------

    def run(self):
        """
        메인 메뉴를 반복해서 실행한다.
        """

        print("Python Quiz Game을 시작합니다.")

        try:
            while True:
                self.show_menu()

                choice = self.get_valid_number(
                    "메뉴를 선택하세요: ", 1, 7
                )

                if choice == 1:
                    self.play_quiz()

                elif choice == 2:
                    self.add_quiz()

                elif choice == 3:
                    self.show_quizzes()

                elif choice == 4:
                    self.show_best_score()

                elif choice == 5:
                    self.delete_quiz()

                elif choice == 6:
                    self.show_history()

                elif choice == 7:
                    self.save_state()
                    print("프로그램을 종료합니다.")
                    break

        except (KeyboardInterrupt, EOFError):
            print("\n프로그램 종료 요청을 확인했습니다.")
            print("현재 데이터를 저장합니다.")
            self.save_state()
            print("안전하게 종료합니다.")

    # ---------------------------------
    # 6. 퀴즈 출제 방식 선택
    # ---------------------------------

    def select_play_mode(self):
        """
        전체 출제, 랜덤 출제, 문제 수 선택 방식을 제공한다.
        """

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return None

        print("\n========== 출제 방식 선택 ==========")
        print("1. 전체 문제 순서대로 풀기")
        print("2. 전체 문제 랜덤으로 풀기")
        print("3. 문제 수 선택해서 풀기")
        print("4. 랜덤으로 문제 수 선택해서 풀기")
        print("0. 메인 메뉴로 돌아가기")

        choice = self.get_valid_number(
            "출제 방식을 선택하세요: ", 0, 4
        )

        if choice == 0:
            return None

        selected_quizzes = self.quizzes.copy()

        # 2번과 4번은 랜덤 출제
        if choice in (2, 4):
            random.shuffle(selected_quizzes)

        # 3번과 4번은 출제 문제 수 선택
        if choice in (3, 4):
            count = self.get_valid_number(
                f"문제 수를 선택하세요 (1~{len(selected_quizzes)}): ",
                1,
                len(selected_quizzes)
            )

            selected_quizzes = selected_quizzes[:count]

        return selected_quizzes

    # ---------------------------------
    # 7. 퀴즈 풀기
    # ---------------------------------


    
    # ---------------------------------
    # 7. 퀴즈 풀기
    # ---------------------------------

    def play_quiz(self):
        """
        선택한 퀴즈를 출제하고 점수를 계산한다.
        힌트를 사용하면 calculate_score()에서 감점한다.
        """

        # 출제 방식 선택
        selected_quizzes = self.select_play_mode()

        if selected_quizzes is None:
            return

        # 게임 진행에 필요한 변수 초기화
        total_questions = len(selected_quizzes)
        total_score = 0
        correct_answers = 0
        hint_count = 0

        print("\n========== 퀴즈 시작 ==========")

        # 선택된 퀴즈를 순서대로 출제
        for index, quiz in enumerate(selected_quizzes, start=1):

            print(f"\n[{index}/{total_questions}]")
            print(quiz.question)

            # 선택지 출력
            for number, choice in enumerate(quiz.choices, start=1):
                print(f"{number}. {choice}")

            # 문제마다 힌트 사용 여부 초기화
            used_hint = False

            # 사용자 입력 및 입력값 검증
            while True:
                answer = input(
                    "정답 번호 입력 (힌트: H, 정답을 모를 경우 Enter): "
                ).strip()

                # 힌트 사용
                if answer.lower() == "h":

                    if used_hint:
                        print("이미 힌트를 사용했습니다.")
                        continue

                    print(f"힌트: {quiz.hint}")
                    used_hint = True
                    hint_count += 1
                    continue

                # Enter를 입력하면 무응답 처리
                if answer == "":
                    answer_number = None
                    break

                # 숫자가 아닌 입력 검사
                if not answer.isdigit():
                    print("정답 번호를 숫자로 입력하세요.")
                    continue

                answer_number = int(answer)

                # 선택지 범위 검사
                if not 1 <= answer_number <= len(quiz.choices):
                    print("선택지 범위 안에서 입력하세요.")
                    continue

                break

            # 정답 여부 확인
            result = quiz.evaluate_answer(answer_number)

            # 이번 문제 점수 계산
            score = quiz.calculate_score(result, used_hint)

            # 전체 점수에 누적
            total_score += score

            # 정답 결과 출력
            if result == "correct":
                print("정답입니다!")
                correct_answers += 1

            elif result == "incorrect":
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")
                quiz.show_answer()

            else:
                print("문제를 건너뛰었습니다.")
                quiz.show_answer()

            # 문제별 점수 출력
            print(f"이번 문제 점수: {score}점")
            print(f"현재 누적 점수: {total_score}점")

        # 최종 점수 계산
        max_score = total_questions * 5

        final_score = max(
            0,
            round((total_score / max_score) * 100)
        )

        # 최종 결과 출력
        print("\n========== 게임 결과 ==========")
        print(f"전체 문제 수: {total_questions}")
        print(f"정답 수: {correct_answers}")
        print(f"힌트 사용 횟수: {hint_count}")
        print(f"획득 점수: {total_score}/{max_score}")
        print(f"최종 점수: {final_score}점")

        # 최고 점수 갱신
        if final_score > self.best_score:
            self.best_score = final_score
            print("새로운 최고 점수를 달성했습니다!")

        # 게임 기록 생성
        record = {
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "score": final_score,
            "hint_count": hint_count
        }

        # 게임 기록 저장
        self.history.append(record)

        # JSON 파일에 데이터 저장
        self.save_state()



    # ---------------------------------
    # 8. 퀴즈 추가
    # ---------------------------------

    def add_quiz(self):
        """
        사용자에게 문제, 선택지, 정답, 힌트를 입력받아 추가한다.
        """

        print("\n========== 퀴즈 추가 ==========")

        question = self.get_valid_text("문제를 입력하세요: ")

        choices = []

        for index in range(4):
            choice = self.get_valid_text(
                f"{index + 1}번 선택지를 입력하세요: "
            )
            choices.append(choice)

        answer = self.get_valid_number(
            "정답 번호를 입력하세요 (1~4): ", 1, 4
        )

        hint = self.get_valid_text("힌트를 입력하세요: ")

        new_quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint
        )

        self.quizzes.append(new_quiz)

        self.save_state()

        print("새로운 퀴즈가 추가되었습니다.")

    # ---------------------------------
    # 9. 퀴즈 목록
    # ---------------------------------

    def show_quizzes(self):
        """
        등록된 모든 퀴즈를 출력한다.
        """

        print("\n========== 퀴즈 목록 ==========")

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[{index}] {quiz.question}")

            for number, choice in enumerate(quiz.choices, start=1):
                print(f"  {number}. {choice}")

    
    # ---------------------------------
    # 10. 퀴즈 삭제
    # ---------------------------------

    def delete_quiz(self):
        """
        선택한 퀴즈를 삭제한다.
        0번을 입력하면 삭제하지 않고 메인 메뉴로 돌아간다.
        삭제 전에 사용자 확인을 받는다.
        """

        # 등록된 퀴즈가 있는지 확인
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        # 퀴즈 목록 출력
        self.show_quizzes()

        # 취소 옵션 안내
        print("\n0. 삭제 취소하고 메인 메뉴로 돌아가기")

        # 삭제할 퀴즈 번호 입력
        quiz_number = self.get_valid_number(
            f"\n삭제할 퀴즈 번호 (0~{len(self.quizzes)}): ",
            0,
            len(self.quizzes)
        )

        # 0번을 입력하면 삭제하지 않고 종료
        if quiz_number == 0:
            print("퀴즈 삭제를 취소했습니다.")
            return

        # 삭제 대상 선택
        target_quiz = self.quizzes[quiz_number - 1]

        print(f"\n삭제 대상: {target_quiz.question}")

        # 삭제 여부 확인
        confirm = self.get_valid_text(
            "정말 삭제하시겠습니까? (y/n): "
        ).lower()

        if confirm == "y":
            self.quizzes.pop(quiz_number - 1)
            self.save_state()
            print("퀴즈가 삭제되었습니다.")

        else:
            print("삭제를 취소했습니다.")


    # ---------------------------------
    # 11. 최고 점수 확인
    # ---------------------------------

    def show_best_score(self):
        """
        지금까지 기록된 최고 점수를 출력한다.
        """

        print("\n========== 최고 점수 ==========")
        print(f"최고 점수: {self.best_score}점")

    # ---------------------------------
    # 12. 점수 기록 확인
    # ---------------------------------

    def show_history(self):
        """
        과거에 플레이한 게임 기록을 출력한다.
        """

        print("\n========== 게임 기록 ==========")

        if not self.history:
            print("저장된 게임 기록이 없습니다.")
            return

        for index, record in enumerate(self.history, start=1):
            print(f"\n[{index}번째 게임]")
            print(f"플레이 시간: {record['played_at']}")
            print(f"문제 수: {record['total_questions']}")
            print(f"정답 수: {record['correct_answers']}")
            print(f"점수: {record['score']}점")
            print(f"힌트 사용: {record['hint_count']}회")
