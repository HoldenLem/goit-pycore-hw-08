def test_parse_input():
    from src.bot.main import parse_input

    assert parse_input("add John 12345") == ("add", "John", "12345")
    assert parse_input("  CHANGE   Alice 67890  ") == ("change", "Alice", "67890")
    assert parse_input("hello") == ("hello",)
    assert parse_input("  exit  ") == ("exit",)
