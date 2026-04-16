from app import app


def test_header_is_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#app-header", timeout=10)
    assert dash_duo.find_element("#app-header").text == "Pink Morsel Sales Visualiser"


def test_visualisation_is_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    assert dash_duo.find_element("#sales-line-chart") is not None


def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-radio", timeout=10)
    radio = dash_duo.find_element("#region-radio")
    text = radio.text.lower()
    for region in ("all", "north", "east", "south", "west"):
        assert region in text
