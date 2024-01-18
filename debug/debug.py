import json
import pdfplumber

path_pdf = "bcc.pdf"


def debug():
    with pdfplumber.open(path_pdf) as pdf:
        pdf.pages[0] = pdf.pages[0].crop(
            bbox=(
                0,
                0.32 * float(pdf.pages[0].height),
                pdf.pages[0].width,
                pdf.pages[0].height,
            )
        )
        page = pdf.pages[0]
        image = page.to_image(resolution=350)
        image.debug_tablefinder(
            {
                "explicit_vertical_lines": [30, 110, 154, 367, 440, 495, 550, 590],
            }
        ).show()

        # debug_image_table = image.debug_tablefinder(
        #     {
        #         "explicit_vertical_lines": [30, 154, 367, 440, 495, 550, 590],
        #     }
        # )

        # image.draw_rects(page_2.extract_words(keep_blank_chars=True))
        # image.show()


def parse_tables():
    data = []

    with pdfplumber.open(path_pdf) as pdf:
        pdf.pages[0] = pdf.pages[0].crop(
            bbox=(
                0,
                0.32 * float(pdf.pages[0].height),
                pdf.pages[0].width,
                pdf.pages[0].height,
            )
        )

        for page_data in pdf.pages:
            table_data = page_data.extract_table(
                table_settings={
                    "explicit_vertical_lines": [30, 154, 367, 440, 495, 550, 590],
                }
            )

            data.append(table_data)
            # table = page_data.extract_table()
            # for row in table:
            # 	if len(row) != 4:
            # 		continue

            # 	date = get_date(row[0])
            # 	if not date:
            # 		continue

            # 	sum = parse_sum(row[1])

            # 	if not sum:
            # 		print("sum is None", row)
            # 		continue

            # 	name_contragent = row[3]

            # 	data.append({"date": date, "sum": sum, "name": name_contragent})

    write_to_file(data, "test.json")
    return data


if __name__ == "__main__":
    debug()

    # parse_tables()
