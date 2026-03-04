import random


def main():
    print("1부터 100까지의 숫자를 맞춰보세요!")
    number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            guess = int(input("숫자를 입력하세요: "))
        except ValueError:
            print("유효한 숫자를 입력해주세요.")
            continue

        attempts += 1

        if guess < number:
            print("너무 작아요.")
        elif guess > number:
            print("너무 커요.")
        else:
            print(f"정답입니다! {attempts}번 만에 맞추셨네요!")
            break


if __name__ == "__main__":
    main()
