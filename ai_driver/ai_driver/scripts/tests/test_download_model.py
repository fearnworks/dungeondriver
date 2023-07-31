import os
import pytest
from ai_driver.scripts.download_model import (
    get_filename_from_url,
    get_output_path,
    write_content_to_file,
    construct_url,
    extract_links,
    update_cursor,
)


# Test get_filename_from_url
def test_get_filename_from_url_should_return_basename_of_url():
    url = "http://example.com/path/to/file.txt"
    assert get_filename_from_url(url) == "file.txt"


# Test get_output_path
def test_get_output_path_should_join_folder_and_filename():
    output_folder = "/path/to/folder"
    filename = "file.txt"
    assert get_output_path(output_folder, filename) == "/path/to/folder/file.txt"


# Test write_content_to_file
def test_write_content_to_file_should_write_content_to_file():
    output_path = "/tmp/test_file.txt"  # Use a temporary file for the test
    data = b"test content"
    write_content_to_file(output_path, data)

    with open(output_path, "rb") as f:
        assert f.read() == data

    os.remove(output_path)  # Clean up the temporary file after the test


# Test construct_url
def test_construct_url_should_return_url_with_cursor_when_cursor_is_provided():
    base = "https://huggingface.co"
    page = "/api/models/model/tree/branch"
    cursor = b"cursor"
    expected_url = "https://huggingface.co/api/models/model/tree/branch?cursor=cursor"
    assert construct_url(base, page, cursor) == expected_url


# Test extract_links
def test_extract_links_should_extract_links_for_pooling_and_dense_directories_and_other_files():
    data_list = [
        {"path": "1_Pooling"},
        {"path": "2_Dense"},
        {"path": "other"},
    ]
    model = "model"
    branch = "branch"
    expected_links = [
        "https://huggingface.co/model/resolve/branch/1_Pooling/config.json",
        "https://huggingface.co/model/resolve/branch/1_Pooling/pytorch_model.bin",
        "https://huggingface.co/model/resolve/branch/2_Dense/config.json",
        "https://huggingface.co/model/resolve/branch/2_Dense/pytorch_model.bin",
        "https://huggingface.co/model/resolve/branch/other",
    ]
    assert extract_links(data_list, model, branch) == expected_links


# Test update_cursor
def test_update_cursor_should_return_base64_encoded_filename_and_cursor_string():
    data_list = [{"path": "file1"}, {"path": "file2"}]
    # The expected_cursor is hardcoded after manually computing the expected result
    expected_cursor = b"ZXlKbWFXeGxYMjVoYldVaU9pSm1hV3hsTWlKOTo1MA%3D%3D"
    assert update_cursor(data_list) == expected_cursor
