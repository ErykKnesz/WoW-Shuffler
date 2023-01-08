import random
import copy
from .. import main
import csv  # optional


PATHS = {
    "horse": "photos/20220529_200810.png",
    "elephant": "photos/20220529_200833.jpg",
    "lion": "photos/20220529_200846.jpg",
    "bear": "photos/20220529_200856.jpg",
    "eagle": "photos/20220529_200910.jpg"
}

wow_shuffler = main.WoWShuffler()
app = main.WoWApp()
shuffling_screen = main.ShufflingScreen()
empires = ['horse', 'bear', 'lion', 'elephant', 'eagle']


def test_shuffle_returns_list():
    assert isinstance(wow_shuffler._shuffle(), list)


def test_shuffle_is_random():
    shuffle_one = wow_shuffler._shuffle()
    shuffle_two = wow_shuffler._shuffle()
    assert shuffle_one != shuffle_two


def test_shuffle_length():
    assert len(wow_shuffler._shuffle()) == 5


def test_shuffled_correctly_with_mode_a_with_empty_devouts():
    wow_shuffler = main.WoWShuffler()
    wow_shuffler.mode = 'a'
    shuffle = wow_shuffler._shuffle()
    assert wow_shuffler._shuffled_correctly(shuffle)


def test_shuffled_correctly_with_mode_a_with_full_devouts():
    wow_shuffler = main.WoWShuffler()
    wow_shuffler.mode = 'a'
    shuffle = wow_shuffler._shuffle()
    wow_shuffler.devouts = shuffle
    assert not wow_shuffler._shuffled_correctly(shuffle)


def test_current_shuffle_with_mode_a_with_random_empire_in_devouts():
    wow_shuffler.mode = 'a'
    answers = []
    wow_shuffler.devouts = random.choices(empires, k=1)
    for i in range(1000):
        wow_shuffler.get_empires_order()
        answer = wow_shuffler.current_shuffle[0] != wow_shuffler.devouts[0]
        answers.append(answer)
    assert all(answers)


def test_current_shuffle_with_mode_b_with_random_empire_in_devouts_and_opposed():
    wow_shuffler = main.WoWShuffler()
    wow_shuffler.mode = 'b'
    answers = []
    wow_shuffler.devouts = random.choices(empires, k=1)
    wow_shuffler.opposed = random.choices(empires, k=1)
    for i in range(1000):
        wow_shuffler.get_empires_order()
        answer = (wow_shuffler.current_shuffle[0] != wow_shuffler.devouts[0]
                  and wow_shuffler.current_shuffle[-1] != wow_shuffler.opposed[0])
        answers.append(answer)
    assert all(answers)


def test_shuffled_correctly_with_mode_b_with_empty_devouts_and_opposed():
    wow_shuffler = main.WoWShuffler()
    wow_shuffler.mode = 'b'
    shuffle = wow_shuffler._shuffle()
    assert wow_shuffler._shuffled_correctly(shuffle)


def test_shuffled_correctly_with_mode_b_with_full_devouts_and_opposed():
    wow_shuffler = main.WoWShuffler()
    wow_shuffler.mode = 'b'
    shuffle = wow_shuffler._shuffle()
    wow_shuffler.devouts = shuffle
    wow_shuffler.opposed = shuffle
    assert not wow_shuffler._shuffled_correctly(shuffle)


def test_get_empires_order_sets_and_returns_current_shuffle():
    shuffle = wow_shuffler.get_empires_order()
    assert wow_shuffler.current_shuffle == shuffle


def test_commit_shuffle_mode_a():
    wow_shuffler.mode = 'a'
    wow_shuffler.current_shuffle = ['horse', 'bear', 'lion', 'elephant', 'eagle']
    wow_shuffler.commit_shuffle()
    assert wow_shuffler.current_shuffle[0] in wow_shuffler.devouts


def test_commit_shuffle_mode_b():
    wow_shuffler.mode = 'b'
    wow_shuffler.current_shuffle = ['horse', 'bear', 'lion', 'elephant', 'eagle']
    wow_shuffler.commit_shuffle()
    assert (wow_shuffler.current_shuffle[0] in wow_shuffler.devouts
            and wow_shuffler.current_shuffle[-1] in wow_shuffler.opposed)


def test_get_current_player():
    for i in range(8):
        wow_shuffler.current_player_index = i
        curr_player = wow_shuffler.get_current_player()
        assert curr_player == wow_shuffler.players[wow_shuffler.current_player_index]


def test_get_next_player_for_index_out_of_range():
    for i in range(4,8):
        wow_shuffler.current_player_index = i
        next_player = wow_shuffler.get_next_player()
        assert next_player == ""


def test_get_next_player_for_index_within_range():
    for i in range(3):
        wow_shuffler.current_player_index = i
        next_player = wow_shuffler.get_next_player()
        assert next_player == wow_shuffler.players[wow_shuffler.current_player_index + 1]


def test_change_player():
    wow_shuffler.current_player_index = random.randint(0, 4)
    wow_shuffler.current_shuffle = wow_shuffler.empires
    current_player_index = copy.deepcopy(wow_shuffler.current_player_index)
    wow_shuffler.change_player()
    next_player_index = wow_shuffler.current_player_index
    
    if current_player_index == 3:
        assert (current_player_index - next_player_index) == 0
    else:
        assert (current_player_index - next_player_index) == -1


def test_reset_properties():
    wow_shuffler.current_player_index = 3
    wow_shuffler.devouts = ['horse']
    wow_shuffler.opposed = ['bear']
    wow_shuffler.current_shuffle = ['horse', 'bear', 'lion', 'elephant', 'eagle']
    wow_shuffler.reset_properties()
    assert all([wow_shuffler.current_player_index == 0,
               wow_shuffler.devouts == [],
               wow_shuffler.opposed == [],
               wow_shuffler.current_shuffle == []])


def test_check_for_images_positive():
    app.check_for_images()
    assert app.use_images


def test_check_for_images_negative():
    main.PATHS = {}
    app = main.WoWApp()
    app.check_for_images()
    assert not app.use_images
    main.PATHS = PATHS


def test_build_returns_screen_manager():
    build = app.build()
    return isinstance(build, main.WoWSceenManager)


def test_update_labels_without_order_images():
    shuffling_screen.update('horse', 'spider')
    assert all([shuffling_screen.player_label == "Current player: horse",
                shuffling_screen.next_player_label == "Next player: spider",
                shuffling_screen.order_label == "Shuffle the loyalty tokens!",
                not shuffling_screen.order_images 
    ])


def test_update_labels_with_order_images():
    shuffling_screen.order_images = empires
    shuffling_screen.update('horse', 'spider')
    assert all([shuffling_screen.player_label == "Current player: horse",
                shuffling_screen.next_player_label == "Next player: spider",
                shuffling_screen.order_label == "Shuffle the loyalty tokens!",
                not all(shuffling_screen.order_images)
    ])


def test_display_order_with_images():
    order = shuffling_screen.display_order(empires)
    as_string = f"{' || '.join(empires)}"
    assert order == (as_string, [PATHS[empire] for empire in empires])


def test_display_order_without_images():
    main.PATHS = {}
    order = shuffling_screen.display_order(empires)
    as_string = f"{' || '.join(empires)}"
    assert order == as_string
    main.PATHS = PATHS