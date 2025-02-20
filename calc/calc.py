# This function adds two numbers
def add(x, y):
    return x + y

# This function subtracts two numbers
def subtract(x, y):
    return x - y

# This function multiplies two numbers
def multiply(x, y):
    return x * y

# This function divides two numbers
def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

operations = {
    '1': (add, '+'),
    '2': (subtract, '-'),
    '3': (multiply, '*'),
    '4': (divide, '/')
}
def main():
    print("Select operation.")
    print("1.Add")
    print("2.Subtract")
    print("3.Multiply")
    print("4.Divide")
    
    while True:
        # take input from the user
        choice = input("Enter choice(1/2/3/4): ")
    
        # check if choice is one of the four options
        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter valid numbers for both inputs.")
                continue
    
            func, operator = operations[choice]
            print(num1, operator, num2, "=", func(num1, num2))
            
            # check if the user wants another calculation
            # break the while loop if answer is no
            while True:
                next_calculation = input("Let's do next calculation? (yes/no): ").lower()
                if next_calculation in ["yes", "no"]:
                    break
            if next_calculation == "no":
                break
        else:
            print("Invalid Input")
            
if __name__ == "__main__":
    main()
