import xlsxwriter

from parse_with_selenium import TimeOfDay

def write_to_excel(forecast, path_to_file):
    workbook = xlsxwriter.Workbook(path_to_file)
    worksheet = workbook.add_worksheet("Прогноз погоды")
    
    formatting_title = workbook.add_format()
    formatting_title.set_bold()
    formatting_title.set_top(2)
    formatting_title.set_bottom()

    row_num = 0
    col_num = 0

    for item in forecast:
        header =[
            item["date"],
            "Температура",
            "Влажность",
            "Давление",
            "Осадки",
            "Доп. информация"
        ]
        for col_title in header:
            worksheet.write(row_num, col_num, col_title, formatting_title)
            col_num += 1
        col_num = 0
        row_num += 1

        table_content = []
        for time_of_day in TimeOfDay:
            tod_key = time_of_day.name

            additional_info = ""

            if time_of_day == TimeOfDay.m:
                additional_info = f"Средняя дневная t°:{item['avg_temp']}°"
            if time_of_day == TimeOfDay.d:
                additional_info = f"Магнитное поле: {item['magnetic']}"
            if time_of_day == TimeOfDay.e:
                additional_info = f"{item['press_changing']}"

            table_content.append([
                time_of_day.value,
                item[tod_key]["temp"],
                item[tod_key]["hum"],
                item[tod_key]["press"],
                item[tod_key]["weather"],
                additional_info
            ])
        
        for row in table_content:
            for col in row:
                worksheet.write(row_num, col_num, col)
                col_num += 1
            col_num = 0
            row_num += 1

        row_num += 1

    worksheet.autofit()
    workbook.close()

    return
