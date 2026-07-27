from monday_api import get_board_data, DEALS_BOARD_ID


def clean_board(board_data):
    rows = []

    boards = board_data.get("data", {}).get("boards", [])

    if not boards:
        print("No boards found!")
        return rows

    items = boards[0]["items_page"]["items"]

    for item in items:
        row = {"Deal": item["name"]}

        for column in item["column_values"]:
            title = column["column"]["title"]
            value = column["text"]

            row[title] = value

        rows.append(row)

    return rows


if __name__ == "__main__":
    data = get_board_data(DEALS_BOARD_ID)

    clean = clean_board(data)

    print(f"Number of rows: {len(clean)}")

    for row in clean:
        print(row)