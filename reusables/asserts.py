
class Assert:
    def __init__():
        pass

    @staticmethod
    def asserts_model(request_data,response):
        expected_data = request_data
        actual_data = response.result.to_dict()

    # Assert that the entire model (the response) matches the expected data
        assert expected_data == actual_data, f"Expected: {expected_data}, but got: {actual_data}"

    @staticmethod
    def assert_equal_ignoring_keys(expected_data, actual_data, keys_to_ignore):
        """
        Asserts equality between two dictionaries/lists, ignoring the specified keys.
        """

        def remove_keys(data, keys_to_remove):
            """
            Recursively removes the specified keys from a dictionary or list of dictionaries.
            """
            if isinstance(data, dict):
                return {key: remove_keys(value, keys_to_remove) for key, value in data.items() if key not in keys_to_remove}
            elif isinstance(data, list):
                return [remove_keys(item, keys_to_remove) for item in data]
            return data
        
        filtered_expected = remove_keys(expected_data, keys_to_ignore)
        filtered_actual = remove_keys(actual_data, keys_to_ignore)
        
        assert filtered_expected == filtered_actual, f"Expected: {filtered_expected}, but got: {filtered_actual}"


