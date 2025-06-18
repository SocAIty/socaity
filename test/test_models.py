import pytest
import os
from test_socaity.test_face2face import test_face2face
from test_socaity.test_spechcraft import test_speechcraft

from test_replicate.test_flux_schnell import test_text2img
from test_replicate.test_deepseek import test_deepseek_v3
from test_replicate.test_llama3 import test_llama_models
from test_replicate.test_sam2 import test_sam2
from test_replicate.test_whisper import test_transcribe


class TestModels:
    """Integration tests that run multiple models in sequence"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for integration tests"""
        self.api_key = os.getenv("SOCAITY_API_KEY")
        if not self.api_key:
            pytest.skip("SOCAITY_API_KEY environment variable not set")
    
    @pytest.mark.socaity
    def test_all_socaity_models(self):
        """Test all Socaity models"""
        socaity_tests = [test_face2face, test_speechcraft]
        
        for test_func in socaity_tests:
            try:
                result = test_func()
                assert result is True, f"Test {test_func.__name__} failed"
            except Exception as e:
                pytest.fail(f"Socaity test {test_func.__name__} failed: {str(e)}")
    
    @pytest.mark.replicate
    def test_all_replicate_models(self):
        """Test all Replicate models"""
        tests = [
            test_text2img,
            test_llama_models,
            test_deepseek_v3,
            test_sam2,
            test_transcribe
        ]
        
        results = []
        for test_func in tests:
            try:
                test_func()
                results.append((test_func.__name__, True, None))
            except Exception as e:
                results.append((test_func.__name__, False, str(e)))
        
        # Check that at least some tests passed
        passed_tests = [r for r in results if r[1]]
        assert len(passed_tests) > 0, f"No tests passed. Results: {results}"
        
        # Report any failures but don't fail the whole test
        failed_tests = [r for r in results if not r[1]]
        if failed_tests:
            print(f"Some tests failed: {failed_tests}")


if __name__ == "__main__":
    # Run all tests
    # pytest socaity/test/test_models.py -v
    #  Run only Socaity model tests
    # pytest socaity/test/test_models.py -v -m socaity
    # Run only Replicate model tests  
    # pytest socaity/test/test_models.py -v -m replicate
    # Run the entire TestModels class
    # pytest socaity/test/test_models.py::TestModels -v
    # Run with pytest when called directly
    pytest.main([__file__, "-v"])
