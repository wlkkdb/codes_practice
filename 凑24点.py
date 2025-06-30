from itertools import permutations, product
import re


def is_valid_number():
    try:
        float()
        return True
    except ValueError:
        return False


def find_24_solution(numbers):
    ops = ['+', '-', '*', '/']
    num_perms = set(permutations(numbers))
    op_perms = list(product(ops, repeat=3))

    templates = [
        # 5种所有可能的括号组合
        '(({0} {1} {2}) {3} {4}) {5} {6}',   # ((a op b) op c) op d
        '({0} {1} ({2} {3} {4})) {5} {6}',   # (a op (b op c)) op d
        '{0} {1} (({2} {3} {4}) {5} {6})',   # a op ((b op c) op d)
        '{0} {1} ({2} {3} ({4} {5} {6}))',   # a op (b op (c op d))
        '(({0} {1} {2}) {3} ({4} {5} {6}))', # ((a op b) op (c op d))
    ]

    solutions = set()

    for nums in num_perms:
        for ops_combo in op_perms:
            for template in templates:
                try:
                    expr = template.format(
                        nums[0], ops_combo[0],
                        nums[1], ops_combo[1],
                        nums[2], ops_combo[2],
                        nums[3]
                    )
                    val = eval(expr)
                    if abs(val - 24) < 1e-6:
                        # 保留括号，便于理解运算顺序
                        expr_std = re.sub(r'\s+', ' ', expr)
                        solutions.add(expr_std)
                except ZeroDivisionError:
                    continue
                except Exception:
                    continue
    return solutions


def get_user_numbers():
    user_input = input("输入需要组合排列的数(用空格分隔):\t").strip()
    if not user_input:
        print("未输入，将使用默认示例 [1, 2, 3, 4]")
        return [1, 2, 3, 4]
    parts = user_input.split()
    if len(parts) != 4:
        print("请输入4个数字。")
        return None
    if not all(is_valid_number(x) for x in parts):
        print("输入包含非数字内容，请重新输入。")
        return None
    return [float(x) for x in parts]


def main():
    numbers = None
    while numbers is None:
        numbers = get_user_numbers()
    solutions = find_24_solution(numbers)
    if solutions:
        print(f"找到 {len(solutions)} 种解法:")
        for i, sol in enumerate(sorted(solutions), 1):
            print(f"{i}. {sol} = 24")
    else:
        print("无法凑出24。")


if __name__ == "__main__":
    main()
