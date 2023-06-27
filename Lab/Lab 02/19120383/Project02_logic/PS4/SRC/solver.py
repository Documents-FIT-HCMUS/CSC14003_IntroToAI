def extract_literals(clause):
    literals = clause.split("OR")

    result = []
    for literal in literals:
        result.append(literal.strip())

    return result


def negate(clause):
    literals = clause.split("OR")

    negations = []
    for literal in literals:
        literal = literal.strip()  # remove trailing spaces

        # if the literal is affirmative, add a "-" to the beginning
        if len(literal) == 1:
            negations.append("-" + literal)

        # if the literal is negative, append the last character to the list
        elif len(literal) == 2:
            negations.append(literal[-1])

    return negations


def is_complementary(literal_1, literal_2):
    # true if both literals' length are not the same and their last characters are not the same
    return (literal_1[-1] == literal_2[-1]) and (len(literal_1) != len(literal_2))


def remove_duplicates(literals):
    result = []
    for literal in literals:
        if literal not in result:
            result.append(literal)
    return result


def literals_sorter(literals):
    result = literals.copy()

    # store negative literals in an array
    negations = []
    for i in range(len(result)):
        if len(result[i]) == 2:
            negations.append(result[i][-1])

    # remove "-" in literals to sort
    for i in range(len(result)):
        if len(result[i]) == 2:
            result[i] = result[i][-1]

    negations.sort(reverse=True)
    result.sort()

    for i in range(len(result)):
        if result[i] in negations:
            negations.pop()
            result[i] = "-" + result[i]

    return result


def create_clause(literals_1, literals_2=None):
    if literals_2 is None:  # code generated by python
        literals_2 = []

    if len(literals_1) == 1 and len(literals_2) == 0:
        return literals_1[0]

    result = literals_1.copy()
    # uniquely merge two lists of literals
    if len(literals_2) != 0:
        for literal in literals_2:
            if literal not in result:
                result.append(literal)

    result = literals_sorter(result)
    result = remove_duplicates(result)
    clause = " OR ".join(result)
    return clause


def pl_resolve(clause_1, clause_2):
    result = []
    flag = False

    literals_1, literals_2 = extract_literals(clause_1), extract_literals(clause_2)

    # find complementary pair
    for i in range(len(literals_1)):
        for j in range(len(literals_2)):
            if is_complementary(literals_1[i], literals_2[j]):
                flag = True
                literals_1.remove(literals_1[i])
                literals_2.remove(literals_2[j])
                break
        if flag:
            break

    # if a complementary pair is found, merge and return a new clause
    if flag:
        if len(literals_1) == 0 and len(literals_2) == 0:
            result.append("{}")
            return result

        literals_1 = literals_sorter(literals_1)
        literals_2 = literals_sorter(literals_2)
        new_clause = create_clause(literals_1, literals_2)
        result.append(new_clause)
        return result

    result.append(clause_1)
    result.append(clause_2)
    return result


def is_always_true(clause):
    literals = extract_literals(clause)
    n = len(literals)

    for i in range(n):
        for j in range(n):
            if is_complementary(literals[i], literals[j]):
                return True
    return False


def is_subset(clauses, new_clauses):
    # to check if "clauses" contain "new_clauses"
    n = len(new_clauses)
    if n == 0:
        return True

    for i in range(n):
        if new_clauses[i] not in clauses:
            return False
    return True


def pl_resolution(knowledge_base, alpha):
    negative_alpha = negate(alpha)
    clauses = []
    clauses.extend(knowledge_base)
    clauses.extend(negative_alpha)

    new_clauses = []
    clause_pairs = []

    records = []
    record = []

    while True:
        n = len(clauses)

        for i in range(n):
            for j in range(i + 1, n):
                clause_pairs.append((clauses[i], clauses[j]))

        for (clause_i, clause_j) in clause_pairs:
            resolvents = pl_resolve(clause_i, clause_j)

            # add resolvents to new_clauses
            for i in range(len(resolvents)):
                # to filter out useless new clauses, such as "A OR -A OR B"
                if not is_always_true(resolvents[i]):
                    if resolvents[i] not in new_clauses:
                        new_clauses.append(resolvents[i])

        if is_subset(clauses, new_clauses):
            records.append(record)
            return False, records

        # add new_clauses to clauses
        for clause in new_clauses:
            # to filter out duplicate new clauses
            if clause not in clauses:
                # to filter out useless new clauses, such as "A OR -A OR B"
                if not is_always_true(clause):
                    clauses.append(clause)
                    record.append(clause)

        records.append(record)
        if "{}" in record:
            return True, records

        record = []
