class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []
        self.funds = 0

        self.total_deposits = 0
        self.total_spent = 0

    def __str__(self):
        line_size = 30
        half = int((line_size - len(self.category)) / 2)
        decorator = "*"
        decoration = decorator * half
        first_line = f"{decoration}{self.category}{decoration}"

        if len(self.ledger) > 0:
            ledger_info = ""
            total = 0
            for item in self.ledger:
                description = item["description"]
                limited_description = description
                if len(description) > 23:
                    limited_description = description[0:23]
                amount = item["amount"]
                total += amount
                amount = f"{amount:.2f}"
                spacing = line_size - len(limited_description) - len(amount)
                ledger_info += f"\n{limited_description}{" " * spacing}{float(amount):.2f}"
            text = f"{first_line}{ledger_info}\nTotal: {total:.2f}"
        else:
            text = f"{first_line}"

        return text

    def deposit(self, amount, description = ""):
        self.funds += amount
        self.total_deposits += amount
        self.ledger.append({"amount": amount, "description": description})
        print(description)
        print(self.ledger)

    def withdraw(self, amount, description = ""):
        if self.check_funds(amount):
            self.funds -= amount
            self.total_spent -= amount
            self.ledger.append({"amount": -amount, "description": description})
            print(description)
            return True
        else:
            return False

    def get_balance(self):
        balance = self.funds
        return float(balance)

    def transfer(self, amount, categoryObject):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {categoryObject.category}")
            categoryObject.deposit(amount, f"Transfer from {self.category}")
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.funds:
            return False
        else:
            return True
        


def create_spend_chart(categories):
    # percentual of the total spent in each category in relation to the total amount spent
    graph = "Percentage spent by category\n"
    longest_name_size = 0
    total_spent_among_all_categories = 0
    for i in categories:
        total_spent_among_all_categories += abs(i.total_spent)

    # graph vertical axis and percentages
    for current_percentage in range(100, -10, -10):
        spacing = 3 - len(str(current_percentage))
        line = f"{" " * spacing}{current_percentage}| "
        for category in categories:
            current_name_length = len(category.category)
            if longest_name_size < current_name_length:
                longest_name_size = current_name_length
            percentage_spent = (abs(category.total_spent) * 100) / total_spent_among_all_categories
            print(f"name: {category.category}, total: {category.total_deposits}, spent: {category.total_spent}, percentage: {percentage_spent}")
            print(f"Ledger: {category.ledger}")
            fill = " " if percentage_spent < current_percentage else "o"
            line += f"{fill}  "
        line += "\n"
        graph += line 
    
    # horizontal axis
    graph += f"{" " * 4}-{"-" * 3 * len(categories)}"

    # category names
    for letter_index in range(longest_name_size):
        line = f"{" " * 5}"
        for item in categories:
            current_character = " "
            if len(item.category) > letter_index:
                current_character = item.category[letter_index]
            line += f"{current_character}{" " * 2}"
        graph += "\n" + line

    print(graph)
    return graph
