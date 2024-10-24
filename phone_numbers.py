import phonenumbers
from phonenumbers import carrier

def get_phone_number_info(phone_number_str):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number_str)

        # Get region code
        region_code = phonenumbers.region_code_for_number(parsed_number)

        # Get carrier name
        carrier_name = carrier.name_for_number(parsed_number, "en")

        # Validate the phone number
        is_valid = phonenumbers.is_valid_number(parsed_number)
        is_possible = phonenumbers.is_possible_number(parsed_number)

        # Format phone number
        international_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)

        return {
            "is_valid": is_valid,
            "is_possible": is_possible,
            "region_code": region_code,
            "carrier": carrier_name,
            "international_format": international_format,
            "national_format": national_format,
        }
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return str(e)

if __name__ == "__main__":
    phone_number_str = "+14155552671"
    result = get_phone_number_info(phone_number_str)

    print(result)
