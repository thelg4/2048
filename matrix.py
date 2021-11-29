# push all non-zero squares in a row to the left
def stack(mat):
    stacked_mat = [[0] * len(mat) for _ in range(len(mat))]
    for i in range(len(mat)):
        fill_pos = 0
        for j in range(len(mat)):
            if mat[i][j] != 0:
                stacked_mat[i][fill_pos] = mat[i][j]
                fill_pos += 1
    return stacked_mat


# reverse matrix rows
def reverse(mat):
    reversed_mat = []
    for i in range(len(mat)):
        reversed_mat.append([])
        for j in range(len(mat)):
            reversed_mat[i].append(mat[i][len(mat) - 1 - j])
    return reversed_mat


# transpose matrix over its diagonal
def transpose(mat):
    transposed_mat = [[0] * len(mat) for _ in range(len(mat))]
    for i in range(len(mat)):
        for j in range(len(mat)):
            transposed_mat[i][j] = mat[j][i]
    return transposed_mat


# combine all adjacent equal squares to the left
def combine(mat):
    score_increment = 0
    for i in range(len(mat)):
        for j in range(len(mat)-1):
            if mat[i][j] != 0 and mat[i][j] == mat[i][j+1]:
                mat[i][j] *= 2
                mat[i][j+1] = 0
                score_increment += mat[i][j]
    return mat, score_increment


# determine whether horizontal move exists from position
def horizontal_move_exists(mat):
    if any(0 in row for row in mat):
        return True
    stacked_mat = stack(mat)
    for i in range(len(mat)):
        for j in range(len(mat)-1):
            if stacked_mat[i][j] == stacked_mat[i][j+1]:
                return True
    return False


# determine whether vertical move exists from position
def vertical_move_exists(mat):
    if any(0 in row for row in mat):
        return True
    stacked_transposed_mat = stack(transpose(mat))
    for i in range(len(mat)):
        for j in range(len(mat)-1):
            if stacked_transposed_mat[i][j] == stacked_transposed_mat[i][j+1]:
                return True
    return False


# indicate whether given state is a win state
def is_win_state(mat, win_score):
    return any(win_score in row for row in mat)


# indicate whether given state is a lose state
def is_lose_state(mat):
    return not horizontal_move_exists(mat) and not vertical_move_exists(mat)


# move left (stack, combine, stack)
def left(mat):
    score_increment = 0
    if horizontal_move_exists(mat):
        mat = stack(mat)
        mat, score_increment = combine(mat)
        mat = stack(mat)
    return mat, score_increment


# move right (reverse, stack, combine, stack, reverse)
def right(mat):
    score_increment = 0
    if horizontal_move_exists(mat):
        mat = reverse(mat)
        mat = stack(mat)
        mat, score_increment = combine(mat)
        mat = stack(mat)
        mat = reverse(mat)
    return mat, score_increment


# move up (transpose, stack, combine, stack, transpose)
def up(mat):
    score_increment = 0
    if vertical_move_exists(mat):
        mat = transpose(mat)
        mat = stack(mat)
        mat, score_increment = combine(mat)
        mat = stack(mat)
        mat = transpose(mat)
    return mat, score_increment


# move down (transpose, reverse, stack, combine, stack, reverse, transpose)
def down(mat):
    score_increment = 0
    if vertical_move_exists(mat):
        mat = transpose(mat)
        mat = reverse(mat)
        mat = stack(mat)
        mat, score_increment = combine(mat)
        mat = stack(mat)
        mat = reverse(mat)
        mat = transpose(mat)
    return mat, score_increment
