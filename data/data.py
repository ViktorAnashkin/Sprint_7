class Data:
    DUPLICATE_LOGIN = "Этот логин уже используется. Попробуйте другой."
    MISSING_FIELDS = "Недостаточно данных для создания учетной записи"
    LOGIN_DATA_MISSING = "Недостаточно данных для входа"
    USER_NOT_FOUND = "Учетная запись не найдена"

order_base = {
    "firstName": "Viktor",
    "lastName": "Anashkin",
    "address": "Lenina, 2 apt.",
    "metroStation": 4,
    "phone": "+7 999 999 99 99",
    "rentTime": 5,
    "deliveryDate": "2026-05-17",
    "comment": "For you comment"
}

order_black = {**order_base, "color": ["BLACK"]}
order_gray = {**order_base, "color": ["GREY"]}
order_both = {**order_base, "color": ["BLACK", "GREY"]}
order_no_color = {**order_base}
