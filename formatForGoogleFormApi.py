from parseCsv import parse_csv

def formatForGoogleFormApi(rows):
    rows_without_header = rows[1:]

    requests = list()

    count = 0

    for row in rows_without_header:
        splitRow = row.split(',')
        splitRow.pop() # remove the correct answer

        requests.append(create_request_item(splitRow, count))

        count += 1

    return requests


def create_request_item(row, index):
    options = list()

    options_inputs = row[1:]

    for item in options_inputs:
        options.append({ "value": item })

    return {
            "createItem": {
                "item": {
                    "title": row[0],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": options,
                                "shuffle": True,
                            },
                        }
                    },
                },
                "location": {"index": index },
            }
        }
