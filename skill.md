# Sample Code Testing Skill

python
def add(a, b):
    """Returns the sum of a and b."""
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    print("All tests passed.")

test_add()