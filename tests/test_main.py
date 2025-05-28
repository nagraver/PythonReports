from main import normalize_field, load_data, print_payout


def test_normalize_field():
    assert normalize_field("Salary") == "rate"
    assert normalize_field("hours_worked") == "hours"
    assert normalize_field("UnknownField") == "unknownfield"
    assert normalize_field("  Name  ") == "name"
    assert normalize_field("EMAIL") == "email"
    assert normalize_field("Hourly_Rate") == "rate"


def test_load_data(tmp_path):
    file = tmp_path / "data.csv"
    file.write_text("Name,Department,Hours,Rate\nAlice,IT,10,15\nBob,HR,8,20")

    data = load_data([str(file)])
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[0]["department"] == "IT"
    assert data[0]["hours"] == "10"
    assert data[0]["rate"] == "15"
    assert data[1]["name"] == "Bob"
    assert data[1]["department"] == "HR"
    assert data[1]["hours"] == "8"
    assert data[1]["rate"] == "20"


def test_load_data_empty_file(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("")
    data = load_data([str(file)])
    assert data == []


def test_load_data_custom_header(tmp_path):
    file = tmp_path / "custom.csv"
    file.write_text("Email,ID,Hours_Worked,Hourly_Rate\nx@x.com,123,5,50")
    data = load_data([str(file)])
    assert data[0]["email"] == "x@x.com"
    assert data[0]["id"] == "123"
    assert data[0]["hours"] == "5"
    assert data[0]["rate"] == "50"


def test_print_payout_output(capsys):
    data = [
        {"name": "Alice", "department": "IT", "hours": "10", "rate": "20"},
        {"name": "Bob", "department": "HR", "hours": "5", "rate": "30"},
    ]
    print_payout(data)
    captured = capsys.readouterr()
    assert "Alice" in captured.out
    assert "Bob" in captured.out
    assert "IT" in captured.out
    assert "HR" in captured.out
    assert "$200" in captured.out
    assert "$150" in captured.out


def test_print_payout_output_with_zero_values(capsys):
    data = [
        {"name": "ZeroHour", "department": "IT", "hours": "0", "rate": "100"},
        {"name": "ZeroRate", "department": "IT", "hours": "10", "rate": "0"},
    ]
    print_payout(data)
    captured = capsys.readouterr()
    assert "ZeroHour" in captured.out
    assert "ZeroRate" in captured.out
    assert "$0" in captured.out
    assert "Total" in captured.out
