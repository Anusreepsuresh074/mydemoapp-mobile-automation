import allure
import pytest

from src.pages.product_page import ProductPage
from src.utils.money import price_value
from tests.product.product_td import COLOUR, LARGE_QUANTITY, REVIEW_THANKS, STARS

pytestmark = allure.feature("Product")


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.p0
@allure.title("PRD-P0-01 Opening a product shows its details")
def test_opening_a_product_shows_its_details(catalog):
    name, price = catalog.first_product()
    product = catalog.open_product(0)
    assert product.name() == name
    assert product.price() == price
    assert product.quantity() == 1


@pytest.mark.regression
@pytest.mark.p1
@pytest.mark.xfail(reason="D-02: the minus button lowers the quantity to 0", strict=True)
@allure.title("PRD-P1-02 Quantity can go up but not below 1 (known defect D-02)")
def test_quantity_goes_up_and_not_below_one(catalog):
    product = catalog.open_product(0)
    product.increase(2)
    assert product.quantity() == 3
    product.decrease(3)
    assert product.quantity() == 1, "quantity went below 1"


@pytest.mark.regression
@pytest.mark.p1
@allure.title("PRD-P1-03 + raises the quantity")
def test_plus_raises_the_quantity(catalog):
    product = catalog.open_product(0)
    product.increase(3)
    assert product.quantity() == 4


@pytest.mark.regression
@pytest.mark.p2
@allure.title("PRD-P2-04 At quantity 0, Add to cart is disabled")
def test_add_to_cart_is_disabled_at_quantity_zero(catalog):
    product = catalog.open_product(0)
    assert product.add_to_cart_enabled()
    product.decrease(1)  # reaches 0 because of D-02
    assert product.quantity() == 0
    assert not product.add_to_cart_enabled(), "Add to cart is still enabled at quantity 0"
    product.press_add_to_cart()
    assert product.header.cart_badge() is None, "a product was added with quantity 0"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("PRD-P2-05 A large quantity is accepted and priced right")
def test_large_quantity_is_priced_right(catalog):
    product = catalog.open_product(0)
    price = price_value(product.price())
    product.increase(LARGE_QUANTITY - 1)
    assert product.quantity() == LARGE_QUANTITY
    product.add_to_cart()
    cart = product.header.open_cart()
    assert cart.item_count() == f"{LARGE_QUANTITY} Items"
    assert price_value(cart.total()) == pytest.approx(LARGE_QUANTITY * price)


@pytest.mark.regression
@pytest.mark.p2
@allure.title("PRD-P2-06 Choosing a colour selects it")
def test_choosing_a_colour_selects_it(catalog):
    product = catalog.open_product(0)
    assert not product.selected_colour_is(COLOUR)
    product.choose_colour(COLOUR)
    assert product.selected_colour_is(COLOUR), f"{COLOUR} is not marked as selected"


@pytest.mark.regression
@pytest.mark.p2
@allure.title("PRD-P2-07 Rating a product shows a thank-you message")
def test_rating_a_product_shows_thanks(catalog):
    product = catalog.open_product(0)
    product.rate(STARS)
    assert product.review_thanks() == REVIEW_THANKS
    product.close_review_message()
    assert product.is_open()


@pytest.mark.regression
@pytest.mark.p0
@pytest.mark.xfail(reason="D-07: opening another product after going back crashes the app", strict=True)
@allure.title("PRD-P0-08 Opening a second product after going back does not crash (known defect D-07)")
def test_opening_a_second_product_after_going_back(app, catalog):
    catalog.open_product(0)
    catalog.go_back()
    assert catalog.is_open()
    second_name = catalog.product_names()[1]
    catalog.find_all(catalog.card_product_image)[1].click()
    product = ProductPage(app)
    assert product.is_open() and product.app_is_in_foreground(), "the app closed (crash)"
    assert product.name() == second_name
