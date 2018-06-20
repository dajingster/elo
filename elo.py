import math


def provisional_probability(R1, R2):

    if R1 <= R2 - 400:
        return 0
    elif R1 >= R2 + 400:
        return 1
    else:
        return 0.5 + (float(R1 - R2)/800)
# Function to calculate the Probability
def standard_probability(R1, R2):

    return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (R2 - R1) / 400))

def K_value(games_played):
    # if games_played < 10:
    #     games_played = 10
    # if games_played > 40:
    #     games_played = 40
    # return 800/games_played
    return 20




def New_Elo(player_a, player_b, result):
	result = float(result)
	a_games = int(player_a[1])
	b_games = int(player_b[1])
	K_a = K_value(a_games)
	K_b = K_value(b_games)
	a_multiplier = 1
	b_multiplier = 1
	current_a = float(player_a[0])
	current_b = float(player_b[0])
	#how to deal with provisional rating
	# if a_games <= 8:
	# 	expected_a = provisional_probability(current_a, current_b)
	# 	b_multiplier = 0.5
	# else:
	expected_a = standard_probability(current_a, current_b)
	# if b_games <= 8:
	# 	expected_b = provisional_probability(current_b, current_a)
	# 	a_multiplier = 0.5
	# else:
	expected_b = standard_probability(current_b, current_a)

	ac_index = a_games
	bc_index = b_games
	if ac_index > 5:
		ac_index = 5

	if bc_index > 5:
		bc_index = 5

	return_values = []
	return_values.append(current_a + (K_a*a_multiplier) * (result - expected_a))
	return_values.append((float(player_a[2])*ac_index + (1 - abs(result - expected_a))**(a_multiplier))/(ac_index + 1))
	return_values.append(current_b + (K_b*b_multiplier) * (1 - result - expected_b))
	return_values.append((float(player_b[2])*bc_index + (1 - abs(result - expected_b))**(b_multiplier))/(bc_index + 1))
	return return_values
