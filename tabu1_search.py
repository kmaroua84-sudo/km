import random

# ==========================================
# 1. Generate Initial Solution
# ==========================================

def generate_initial_solution(weights, capacity):

    n = len(weights)
    solution = [0] * n

    indices = list(range(n))
    random.shuffle(indices)

    total_weight = 0

    for i in indices:
        if total_weight + weights[i] <= capacity:
            solution[i] = 1
            total_weight += weights[i]

    return solution


# ==========================================
# 2. Calculate Total Profit
# ==========================================

def calculate_profit(solution, profits):

    return sum(
        profits[i] * solution[i]
        for i in range(len(solution))
    )


# ==========================================
# 3. Calculate Total Weight
# ==========================================

def calculate_weight(solution, weights):

    return sum(
        weights[i] * solution[i]
        for i in range(len(solution))
    )


# ==========================================
# 4. Generate Neighborhood
#    Add, Remove and Swap
# ==========================================

def generate_neighbors(solution, profits, weights, capacity):

    neighbors = []
    n = len(solution)

    # ADD MOVE
    for i in range(n):

        if solution[i] == 0:

            neighbor = solution.copy()
            neighbor[i] = 1

            if calculate_weight(neighbor, weights) <= capacity:

                move = ("Add", i)

                neighbors.append(
                    (neighbor, calculate_profit(neighbor, profits), move)
                )

    # REMOVE MOVE
    for i in range(n):

        if solution[i] == 1:

            neighbor = solution.copy()
            neighbor[i] = 0

            move = ("Remove", i)

            neighbors.append(
                (neighbor, calculate_profit(neighbor, profits), move)
            )

    # SWAP MOVE
    for i in range(n):

        if solution[i] == 1:

            for j in range(n):

                if solution[j] == 0:

                    neighbor = solution.copy()
                    neighbor[i] = 0
                    neighbor[j] = 1

                    if calculate_weight(neighbor, weights) <= capacity:

                        move = ("Swap", i, j)

                        neighbors.append(
                            (neighbor, calculate_profit(neighbor, profits), move)
                        )

    return neighbors


# ==========================================
# 5. Get Reverse Move
# ==========================================

def get_reverse_move(move):

    if move[0] == "Add":
        return ("Remove", move[1])

    elif move[0] == "Remove":
        return ("Add", move[1])

    elif move[0] == "Swap":
        return ("Swap", move[2], move[1])


# ==========================================
# 6. Tabu Search Algorithm
# ==========================================

def tabu_search(
    profits,
    weights,
    capacity,
    tabu_tenure,
    max_iter,
    max_no_improve
):

    current_solution = generate_initial_solution(weights, capacity)
    best_solution = current_solution.copy()

    tabu_list = {}

    iteration = 0
    no_improvement = 0

    print("\n========== INITIAL SOLUTION ==========")
    print("Initial solution:", current_solution)
    print("Initial profit:", calculate_profit(current_solution, profits))
    print("Initial weight:", calculate_weight(current_solution, weights))

    # MAIN LOOP
    while iteration < max_iter and no_improvement < max_no_improve:

        iteration += 1

        print("\n========== ITERATION", iteration, "==========")

        # Remove expired tabu moves
        tabu_list = {
            move: expiry
            for move, expiry in tabu_list.items()
            if expiry >= iteration
        }

        # Generate neighbors
        neighbors = generate_neighbors(
            current_solution,
            profits,
            weights,
            capacity
        )

        print("Number of neighbors:", len(neighbors))

        if not neighbors:
            print("No neighbors available. Search stopped.")
            break

        # Sort neighbors by decreasing profit
        neighbors.sort(key=lambda x: x[1], reverse=True)

        print("\nSorted Neighbors:")

        for neighbor, profit, move in neighbors:

            print(
                "Solution:", neighbor,
                "| Profit:", profit,
                "| Weight:", calculate_weight(neighbor, weights),
                "| Move:", move
            )

        # Select best admissible neighbor
        selected_neighbor = None

        best_profit = calculate_profit(best_solution, profits)

        print("\n----- Tabu Test and Aspiration -----")

        for neighbor, profit, move in neighbors:

            print("\nTesting move:", move)

            is_tabu = move in tabu_list

            # Aspiration Criterion
            if is_tabu and profit > best_profit:

                print("Aspiration criterion satisfied: Accepted.")

                selected_neighbor = (neighbor, profit, move)
                break

            elif not is_tabu:

                print("Move is not Tabu: Accepted.")

                selected_neighbor = (neighbor, profit, move)
                break

            else:

                print("Move is Tabu and Aspiration is not satisfied.")

        # Stop if no admissible neighbor exists
        if selected_neighbor is None:

            print("\nNo admissible neighbor. Search stopped.")
            break

        # Update current solution
        current_solution = selected_neighbor[0].copy()
        accepted_move = selected_neighbor[2]

        print("\nNew current solution:", current_solution)

        current_profit = calculate_profit(current_solution, profits)

        print("Current profit:", current_profit)

        # Update best solution
        if current_profit > best_profit:

            best_solution = current_solution.copy()
            no_improvement = 0

            print("Best solution updated:", best_solution)

        else:

            no_improvement += 1

            print("No improvement.")
            print("Consecutive iterations without improvement:",
                  no_improvement)

        # Update Tabu List
        reverse_move = get_reverse_move(accepted_move)

        tabu_list[reverse_move] = iteration + tabu_tenure

        print("\nAccepted move:", accepted_move)
        print("Forbidden reverse move:", reverse_move)

        print("Tabu List:")

        for move, expiry in tabu_list.items():

            print(move, "| Forbidden until iteration:", expiry)

    # ==========================================
    # 7. Final Results
    # ==========================================

    print("\n========== FINAL RESULT ==========")

    print("Best solution:", best_solution)

    print("Total profit:",
          calculate_profit(best_solution, profits))

    print("Total weight:",
          calculate_weight(best_solution, weights))

    print("Number of iterations:", iteration)

    print("Final Tabu List:", tabu_list)

    return best_solution


# ==========================================
# 8. Input Data
# ==========================================

print("===== 0-1 KNAPSACK PROBLEM =====")

n = int(input("Enter the number of items: "))

profits = []
weights = []

for i in range(n):

    print("\nItem", i + 1)

    p = float(input("Enter profit: "))
    w = float(input("Enter weight: "))

    if p < 0 or w <= 0:
        raise ValueError("Profits must be non-negative and weights positive.")

    profits.append(p)
    weights.append(w)

capacity = float(input("\nEnter knapsack capacity: "))

if capacity < 0:
    raise ValueError("Capacity must be non-negative.")

tabu_tenure = int(input("Enter Tabu Tenure: "))
max_iter = int(input("Enter maximum iterations: "))
max_no_improve = int(input("Enter maximum iterations without improvement: "))

if tabu_tenure < 1 or max_iter < 1 or max_no_improve < 1:
    raise ValueError("All parameters must be positive.")


# ==========================================
# 9. Run Algorithm
# ==========================================

best_solution = tabu_search(
    profits,
    weights,
    capacity,
    tabu_tenure,
    max_iter,
    max_no_improve
)
