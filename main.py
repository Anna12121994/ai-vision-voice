import os

from vision import analyze_image
from voice import generate_speech


SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png"]
last_description = ""


def save_description(image_path, description):
    with open("descriptions.txt", "a", encoding="utf-8") as file:
        file.write(f"Image: {image_path}\n")
        file.write(f"Description: {description}\n")
        file.write("-----------------------------\n")


def check_image(image_path):
    if not os.path.exists(image_path):
        print("Файл не знайдено.")
        return False

    extension = os.path.splitext(image_path)[1].lower()

    if extension not in SUPPORTED_FORMATS:
        print("Непідтримуваний формат.")
        print("Доступні формати: JPG, JPEG, PNG")
        return False

    return True


def analyze_new_image():
    global last_description

    print()
    print(" ANALYZE IMAGE ")

    image_path = input("Enter image path: ")

    if not check_image(image_path):
        return

    try:
        print()
        print("Analyzing image...")

        description = analyze_image(image_path)

        if not description:
            print("Модель не змогла створити опис.")
            return

        last_description = description

        print()
        print("Image description:")
        print(description)

        save_description(
            image_path,
            description
        )

        print()
        print("Generating speech...")

        output_path = "output/description.wav"

        generate_speech(
            description,
            output_path
        )

        print()

        print("Task completed successfully!")


        print("Image:", image_path)
        print("Description:", description)
        print(
            "Vision model:",
            "Salesforce/blip-image-captioning-base"
        )
        print(
            "TTS model:",
            "facebook/mms-tts-eng"
        )
        print(
            "Audio saved to:",
            output_path
        )

    except Exception as error:
        print()
        print("Сталася помилка:")
        print(error)


def repeat_speech():
    global last_description

    print()
    print(" REPEAT SPEECH ")

    if not last_description:
        print("Немає опису для повторного озвучення.")
        print("Спочатку проаналізуйте фотографію.")
        return

    filename = input(
        "Введіть назву WAV-файлу без розширення: "
    )

    if not filename:
        filename = "repeat_description"

    output_path = f"output/{filename}.wav"

    try:
        print("Generating speech...")

        generate_speech(
            last_description,
            output_path
        )

        print("Audio saved to:", output_path)

    except Exception as error:
        print("Помилка генерації аудіо:")
        print(error)


def show_last_description():
    global last_description

    print()
    print(" LAST DESCRIPTION ")

    if last_description:
        print(last_description)
    else:
        print("Опису ще немає.")


def main():
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    while True:
        print()

        print("   AI VISION & VOICE ASSISTANT")

        print("1. Проаналізувати фотографію")
        print("2. Повторно озвучити опис")
        print("3. Показати останній опис")
        print("0. Вихід")

        choice = input("Оберіть пункт: ")

        if choice == "1":
            analyze_new_image()

        elif choice == "2":
            repeat_speech()

        elif choice == "3":
            show_last_description()

        elif choice == "0":
            print("Програму завершено.")
            break

        else:
            print("Невірний пункт меню.")


main()