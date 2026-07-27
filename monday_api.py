import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MONDAY_API_KEY")
DEALS_BOARD_ID = os.getenv("DEALS_BOARD_ID")
WORK_ORDERS_BOARD_ID = os.getenv("WORK_ORDERS_BOARD_ID")

URL = "https://api.monday.com/v2"

HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}


def get_board_data(board_id):
    query = f"""
    query {{
      boards(ids: {board_id}) {{
        id
        name
        items_page(limit: 100) {{
          items {{
            id
            name
            column_values {{
              column {{
                title
              }}
              text
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        URL,
        json={"query": query},
        headers=HEADERS
    )

    return response.json()


if __name__ == "__main__":
    deals = get_board_data(DEALS_BOARD_ID)
    print(deals)