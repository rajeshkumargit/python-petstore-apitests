import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Assert:
    def __init__(self):
        pass

    @staticmethod
    def asserts_model(request_data, response):
        """
        Asserts that the entire model (the response) matches the expected data.
        """
        expected_data = request_data
        actual_data = response.result.to_dict()
        
        logger.info(f"Asserting model. Expected data: {expected_data}, Actual data: {actual_data}")

        assert expected_data == actual_data, f"Expected: {expected_data}, but got: {actual_data}"
        logger.info("Model assertion passed")

    @staticmethod
    def assert_equal_ignoring_keys(expected_data, actual_data, keys_to_ignore):
        """
        Asserts equality between two dictionaries/lists, ignoring the specified keys.
        """
        logger.info(f"Asserting equality ignoring keys. Expected data: {expected_data}, Actual data: {actual_data}, Keys to ignore: {keys_to_ignore}")

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
        
        logger.info(f"Filtered expected data: {filtered_expected}, Filtered actual data: {filtered_actual}")

        assert filtered_expected == filtered_actual, f"Expected: {filtered_expected}, but got: {filtered_actual}"
        logger.info("Equality assertion passed")
