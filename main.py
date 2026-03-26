from dataset_organizer import process_csv

session = process_csv(
    file="dataset_mandatory.csv",
)

if session:
    print(f"Парсинг завершен! Результат: {session}")