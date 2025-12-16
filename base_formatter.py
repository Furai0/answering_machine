def convert_emails_compact(input_file, output_file):

    try:
        with open(input_file, 'r', encoding='windows-1251') as f:
            emails = [line.strip() for line in f if line.strip()]

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"words = {emails}\n")

            print(f"Сохранено {len(emails)} email-адресов в {output_file}")
        return emails

    except Exception as e:
        print(f"Ошибка: {e}")


convert_emails_compact("russian.txt", "russian123.py")