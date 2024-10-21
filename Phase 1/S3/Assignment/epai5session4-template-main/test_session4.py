import pytest
import re
import inspect
import random
import os
import math
from decimal import *

import session4
from session4 import Qualean

README_CONTENT_CHECK_FOR = [
    "and",
    "or",
    "repr",
    "str",
    "add",
    "eq",
    "float",
    "ge",
    "gt",
    "invert",
    "le",
    "lt",
    "mul",
    "sqrt",
    "bool",
    "init"
]

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(session4)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(session4, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

def test_qualean_repr():
    q = session4.Qualean()
    assert q.__repr__() == f'Qualean Class Instance', 'The representation of the Qualean object does not meet expectations'

def test_qualean_str():
    q = session4.Qualean()
    assert q.__str__() == f'Qualean String for number: ' + str(q.number), 'The print of the Qualean object does not meet expectations'

def test_function_qualean_type():
    q = session4.Qualean()
    assert isinstance(q, session4.Qualean), 'Check your type, its not Qualean'

def test_qualean_decimal_precision():
    q = session4.Qualean().return_qualean()
    if q != 0:
        assert len(str(q).split('.')[-1]) == 10, 'Rounding to specified precision is not happening'
    else:
        assert len(str(q).split('.')[-1]) == 1, 'Rounding to specified precision is not happening'

def test_function_count():
    functions = inspect.getmembers(test_session4, inspect.isfunction)
    assert len(functions) > 25, 'Test cases seems to be low. Work harder man...'

def test_function_repeatations():
    functions = inspect.getmembers(test_session4, inspect.isfunction)
    names = []
    for function in functions:
        names.append(function)
    assert len(names) == len(set(names)), 'Test cases seems to be repeating...'

def test_100_qualeans():
    q = session4.Qualean().return_qualean()
    sum = 0
    for i in range(100):
        sum = sum + q
    assert round(sum, 10) == round(100 * q, 10), 'Test case for 100 times Qualean failed'

def test_function_sqrt():
    q = session4.Qualean()
    if q.return_qualean() >= 0:
        assert round(q.__sqrt__(), 10) == round(Decimal(q.return_qualean()).sqrt(), 10), 'Test case for sqrt method failed...'
    else:
        assert q.__sqrt__() == str(round(Decimal(q.__invertsign__()).sqrt(), 10)) + 'i', "Qualean sqrt failed for negative qualeans..."

def test_million_qualeans_sum():
    sum = 0
    for i in range(1000000):
        sum = sum + session4.Qualean().return_qualean()
    assert math.isclose(sum, 0.0) == False, 'Test case for MILLION Qualeans addition failed'

def test_million_qualeans_mul():
    sum = 1
    for i in range(1000000):
        sum = sum * session4.Qualean().return_qualean()
    assert math.isclose(sum, 0.0) == True, 'Test case for MILLION Qualeans multiplication failed'

def test_qualean_valid_input():
    with pytest.raises(ValueError):
        q1 = session4.Qualean(10)
    with pytest.raises(ValueError):
        q1 = session4.Qualean(-10)
    with pytest.raises(ValueError):
        q1 = session4.Qualean(2)

def test_invalid_input_valueerror_provides_relevant_message():
    with pytest.raises(ValueError, match=r".*[-1,0,1].*"):
        q = session4.Qualean(10)

def test_qualean_validity():
    q1 = session4.Qualean()
    q2 = session4.Qualean(1)
    q3 = session4.Qualean(-1.0)
    assert isinstance(q1, session4.Qualean) and q1.__float__() < 1 and q1.__float__() > -1, 'Not generated valid Qualean...'
    assert isinstance(q2, session4.Qualean) and q2.__float__() < 1 and q1.__float__() > -1, 'Not generated valid Qualean...'
    assert isinstance(q3, session4.Qualean) and q3.__float__() < 1 and q1.__float__() > -1, 'Not generated valid Qualean...'

def test_function_and():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    if q1.return_qualean() == 0 or q2.return_qualean() == 0:
        assert q1.__and__(q2) == False, 'Qualean and operation failed when one of them is false...'
    else:
        assert q1.__and__(q2) == True, 'Qualean and operation failed when none of them is false..'

def test_and_q_notdefined():
    q1 = session4.Qualean()
    q2 = None
    assert q1.__and__(q2) == False, "Second Qualean not defined in and operation..."

def test_and_q_false():
    q1 = session4.Qualean(0)
    q2 = session4.Qualean()
    assert q1.__and__(q2) == False, "First Qualean is false in and operation..."

def test_function_or():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    if q1.return_qualean() == 0 and q2.return_qualean() == 0:
        assert q1.__or__(q2) == False, 'Qualean or operation failed when both qualeans are false...'
    else:
        assert q1.__or__(q2) == True, 'Qualean or operation failed when at least one qualean is true...'

def test_or_q_notdefined():
    q1 = session4.Qualean()
    q2 = None
    assert q1.__or__(q2) == True, "Second Qualean not defined in or operation..."

def test_or_q_false():
    q1 = session4.Qualean(1)
    q2 = session4.Qualean()
    assert q1.__or__(q2) == True, "First Qualean is true in or operation..."

def test_function_add():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    assert q1.__add__(q2) == q1.return_qualean() + q2.return_qualean() , 'This is how you mess up simple addition...'

def test_function_add_non_qualean():
    q1 = session4.Qualean()
    q2 = random.uniform(-1000,1000)
    assert q1.__add__(q2) == q1.return_qualean() + q2 , 'This is how you mess up simple addition...'

def test_function_mul():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    assert q1.__mul__(q2) == q1.return_qualean() * q2.return_qualean() , 'This is how you mess up simple multiplication...'

def test_function_mul_non_qualean():
    q1 = session4.Qualean()
    q2 = random.uniform(-1000,1000)
    assert q1.__mul__(q2) == q1.return_qualean() * q2 , 'This is how you mess up simple multiplication...'

def test_function_ge():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    assert q1.__ge__(q2) == (q1.return_qualean() >= q2.return_qualean()),'Qualean ge method failed. q1 should be greater than equal to q2'

def test_function_ge_non_qualean():
    q1 = session4.Qualean()
    q2 = random.uniform(-1000,1000)
    assert q1.__ge__(q2) == (q1.return_qualean() >= q2),'Non Qualean ge method failed. q1 should be greater than equal to q2'

def test_function_gt():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    assert q1.__gt__(q2) == (q1.return_qualean() > q2.return_qualean()),'Qualean gt method failed. q1 should be greater than q2'

def test_function_gt_non_qualean():
    q1 = session4.Qualean()
    q2 = random.uniform(-1000,1000)
    assert q1.__gt__(q2) == (q1.return_qualean() > q2),'Non Qualean gt method failed. q1 should be greater than q2'

def test_function_le():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    assert q1.__le__(q2) == (q1.return_qualean() <= q2.return_qualean()),'Qualean le method failed. q1 should be less than equal to q2'

def test_function_le_non_qualean():
    q1 = session4.Qualean()
    q2 = random.uniform(-1000,1000)
    assert q1.__le__(q2) == (q1.return_qualean() <= q2),'Non Qualean le method failed. q1 should be less than equal to q2'

def test_function_lt():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    assert q1.__lt__(q2) == (q1.return_qualean() < q2.return_qualean()),'Qualean lt method failed. q1 should be less than q2'

def test_function_lt_non_qualean():
    q1 = session4.Qualean()
    q2 = random.uniform(-1000,1000)
    assert q1.__lt__(q2) == (q1.return_qualean() < q2),'Non Qualean lt method failed. q1 should be less than q2'

def test_function_with_non_number():
    q1 = session4.Qualean()
    q2 = 'session4.Qualean()'

    with pytest.raises(TypeError):
        q1.__add__(q2)
    with pytest.raises(TypeError):
        q1.__mul__(q2)
    with pytest.raises(TypeError):
        q1.__eq__(q2)
    with pytest.raises(TypeError):
        q1.__ge__(q2)
    with pytest.raises(TypeError):
        q1.__gt__(q2)
    with pytest.raises(TypeError):
        q1.__le__(q2)
    with pytest.raises(TypeError):
        q1.__lt__(q2)

def test_function_bool():
    q = session4.Qualean()
    assert q.__bool__() == bool(q.return_qualean()), 'Qualean bool is going haywire...'

def test_function_eq():
    q1 = session4.Qualean()
    q2 = session4.Qualean()
    if(q1.return_qualean() == q2.return_qualean()):
        assert q1.__eq__(q2) == True, "Qualean equality failed..."
    else:
        assert q1.__eq__(q2) == False, "Qualean equality failed..."

def test_function_float():
    q = session4.Qualean()
    assert isinstance(q.__float__(), float), "Test case for float conversion failed"

def test_function_invertsign():
    q = session4.Qualean()
    assert q.__invertsign__() == -q.return_qualean(), "Test case for invert sign failed"
