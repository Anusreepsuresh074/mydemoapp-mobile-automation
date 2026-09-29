"""The four checkout screens: address, payment, review, complete."""

from src.core.base_screen import BaseScreen
from src.screens.mydemoapp._ids import rid


class AddressScreen(BaseScreen):
    input_full_name = rid("fullNameET")
    input_address_1 = rid("address1ET")
    input_address_2 = rid("address2ET")
    input_city = rid("cityET")
    input_zip = rid("zipET")
    input_state = rid("stateET")
    input_country = rid("countryET")
    btn_to_payment = rid("paymentBtn")
    msg_full_name_error = rid("fullNameErrorTV")
    msg_address_error = rid("address1ErrorTV")
    msg_city_error = rid("cityErrorTV")


class PaymentScreen(BaseScreen):
    input_card_name = rid("nameET")
    input_card_number = rid("cardNumberET")
    input_expiry = rid("expirationDateET")
    input_security_code = rid("securityCodeET")
    chk_billing_same = rid("billingAddressCB")
    btn_review_order = rid("paymentBtn")


class ReviewScreen(BaseScreen):
    txt_heading = rid("enterShippingAddressTV")
    txt_item_name = rid("titleTV")
    txt_full_name = rid("fullNameTV")
    txt_address = rid("addressTV")
    txt_card_holder = rid("cardHolderTV")
    txt_item_count = rid("itemNumberTV")
    txt_total = rid("totalAmountTV")
    btn_place_order = rid("paymentBtn")


class CompleteScreen(BaseScreen):
    txt_complete = rid("completeTV")
    txt_thank_you = rid("thankYouTV")
    btn_continue_shopping = rid("shoopingBt")
