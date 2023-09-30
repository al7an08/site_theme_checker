import requests
import openpyxl

# Список URL-адресов, на которые нужно отправить GET-запросы
urls = []

# Открываем файл XLSX
workbook1 = openpyxl.load_workbook('change_saits.xlsx')

# Получаем активный лист (можно указать имя листа, если он не активен)
sheet = workbook1.active



# Проходимся по строкам листа и собираем данные в массив
for row in sheet.iter_rows(values_only=True):
    url = f'http://127.0.0.1:5000/check_domain?domain={row[0]}'
    urls.append(url)

# Создайте новую книгу Excel и активный лист
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Заголовки столбцов
worksheet['A1'] = 'URL'
worksheet['B1'] = 'Response'

# Отправьте GET-запросы и запишите ответы в таблицу

for index, url in enumerate(urls, start=2):
    response = requests.get(url)
    print(url)
    worksheet[f'A{index}'] = url
    worksheet[f'B{index}'] = response.text
    if index==70:
        break

# Сохраните книгу в файл XLSX
workbook.save('responses.xlsx')

# Закройте книгу
workbook.close()

print("Ответы записаны в файл responses.xlsx")