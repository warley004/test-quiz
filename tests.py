import pytest
from model import Choice, Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_choice_accepts_valid_text_and_id():
    choice = Choice(id=10, text='answer')

    assert choice.id == 10
    assert choice.text == 'answer'
    assert not choice.is_correct


def test_choice_can_be_created_as_correct():
    choice = Choice(id=1, text='answer', is_correct=True)

    assert choice.is_correct


def test_choice_rejects_empty_text():
    with pytest.raises(Exception, match='Text cannot be empty'):
        Choice(id=1, text='')


def test_choice_rejects_text_longer_than_100_characters():
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        Choice(id=1, text='a' * 101)


def test_added_choices_receive_sequential_ids():
    question = Question(title='q1')

    first_choice = question.add_choice('first')
    second_choice = question.add_choice('second')

    assert [first_choice.id, second_choice.id] == [1, 2]


def test_remove_choice_by_id_removes_only_requested_choice():
    question = Question(title='q1')
    first_choice = question.add_choice('first')
    question.add_choice('second')

    question.remove_choice_by_id(first_choice.id)

    assert [choice.text for choice in question.choices] == ['second']


def test_remove_choice_by_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('first')

    with pytest.raises(Exception, match='Invalid choice id 2'):
        question.remove_choice_by_id(2)


def test_remove_all_choices_empties_question():
    question = Question(title='q1')
    question.add_choice('first')
    question.add_choice('second')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices_marks_requested_choices():
    question = Question(title='q1')
    first_choice = question.add_choice('first')
    second_choice = question.add_choice('second')

    question.set_correct_choices([second_choice.id])

    assert not first_choice.is_correct
    assert second_choice.is_correct


def test_correct_selected_choices_returns_only_correct_selection_ids():
    question = Question(title='q1', max_selections=2)
    correct_choice = question.add_choice('correct', is_correct=True)
    incorrect_choice = question.add_choice('incorrect')

    selected_correct_ids = question.correct_selected_choices(
        [correct_choice.id, incorrect_choice.id]
    )

    assert selected_correct_ids == [correct_choice.id]
