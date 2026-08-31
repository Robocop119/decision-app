def calculate_score(criteria, scores):
    total = 0

    for criterion in criteria:
        criterion_id = criterion[0]
        weight = criterion[2]

        for score in scores:
            if score[1] == criterion_id:
                total += score[2] * weight

    return total
