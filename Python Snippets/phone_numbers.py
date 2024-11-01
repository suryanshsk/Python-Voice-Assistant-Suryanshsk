import phonenumbers
from phonenumbers import carrier, timezone, geocoder, number_type, PhoneNumberType

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
        rfc3966_format = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.RFC3966)
        
        #Advanced Information
        number_timezones = timezone.time_zones_for_number(parsed_number)
        location = geocoder.description_for_number(parsed_number, "en")
        
        # Map of phone number types
        number_type_map = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed Line",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-Free",
            phonenumbers.PhoneNumberType.VOIP: "VoIP",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
            phonenumbers.PhoneNumberType.SHARED_COST: "Shared Cost",
            phonenumbers.PhoneNumberType.UNKNOWN: "Unknown",
        }
        
        # Get the number type as a string
        number_type_value = phonenumbers.number_type(parsed_number)
        number_type_str = number_type_map.get(number_type_value, "Unknown")
        
        #User-friendly messages and suggestions
        valid_msg = "This is a valid phine number." if is_valid else "/this is not a valid phone number"
        possible_msg = "This phone number is possible." if is_possible else "This phone number is not possible"
        suggestion_msg = ""
        
        if not is_valid or not is_possible:
            suggestion_msg = "Please check the number and ensure it includes the correct country code"
            

        return {
            "Validation": valid_msg,
            "Possibility": possible_msg,
            "Region Code": region_code,
            "Carrier": carrier_name or "Carrier information not available",
            "International Format": international_format,
            "National Format": national_format,
            "RFC3966 Format": rfc3966_format,
            "Timezones": number_timezones or "Timezone information not available",
            "Geographical Location": location or "Location information not available",
            "Number Type": number_type_str or "Number type information not available",
            "Suggestions": suggestion_msg
        }
        
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return {"Error": f"Invalid input: {str(e)}. Please enter a valid phone number with country code"}

if __name__ == "__main__":
    phone_number_str = "+14155552671"
    result = get_phone_number_info(phone_number_str)

    for key, value in result.items():
        print(f"{key}: {value}")
