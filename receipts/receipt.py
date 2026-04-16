import json

NDS_RATE = 0.2
DISCOUNT_THRESHOLD = 10000
DISCOUNT = 0.1


def load_receipts():
    with open("receipts.json", "r", encoding="utf-8") as f:
        return json.load(f)


def validate(items):
    if not items:
        raise ValueError("Чек не должен быть пустой")

    for item in items:
        if item["price"] <= 0:
            raise ValueError("Цена должна быть > 0")


def calculate(items):
    subtotal = sum(i["price"] for i in items)

    if subtotal > DISCOUNT_THRESHOLD:
        subtotal_after_discount = subtotal * (1 - DISCOUNT)
    else:
        subtotal_after_discount = subtotal

    nds = subtotal_after_discount * NDS_RATE
    total = subtotal_after_discount + nds

    return subtotal, subtotal_after_discount, nds, total


def print_receipt(data):
    items = data["items"]
    payment = data["payment"]

    validate(items)
    subtotal, discounted, nds, total = calculate(items)

    print("=" * 40)
    print("        СК - НЕчемпион")
    print("=" * 40)

    for item in items:
        print(f"{item['name']:<25}{item['price']:>10.2f}")

    print("-" * 40)
    print(f"{'Подытог:':<25}{subtotal:>10.2f}")
    print(f"{'Со скидкой:':<25}{discounted:>10.2f}")
    print(f"{'НДС 20%:':<25}{nds:>10.2f}")
    print(f"{'ИТОГО:':<25}{total:>10.2f}")
    print("-" * 40)
    print(f"{'Оплата:':<25}{payment:>10}")
    print("=" * 40)


if __name__ == "__main__":
    receipts = load_receipts()
    for r in receipts:
        print_receipt(r)