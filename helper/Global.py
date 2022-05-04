import os

from pyzip import PyZip

bad_functions = {
        'eval': r'eval\(([\s]*)(.*?)([\s]*)\)',
        'system': r'system\(([\s]*)(.*?)([\s]*)\)',
        'chmod': r'chmod\(([\s]*)(.*?)([\s]*)\)',
        'fileperms': r'fileperms\(([\s]*)(.*?)([\s]*)\)',
        'unlink': r'unlink\(([\s]*)(.*?)([\s]*)\)',
        'mkdir': r'mkdir\(([\s]*)(.*?)([\s]*)\)',
        'assert': r'assert\(([\s]*)(.*?)([\s]*)\)',
        'base64_decode': r'base64_decode\(([\s]*)(.*?)([\s]*)\)',
        'file_get_contents': r'file_get_contents\(([\s]*)(.*?)([\s]*)\)',
        'file_put_contents': r'file_put_contents\(([\s]*)(.*?)([\s]*)\)',
        'curl_exec': r'curl_exec\(([\s]*)(.*?)([\s]*)\)',
        'curl_multi_exec': r'curl_multi_exec\(([\s]*)(.*?)([\s]*)\)',
        'move_uploaded_file': r'move_uploaded_file\(([\s]*)(.*?)([\s]*)\)',
    }
bad_functions_wp = {
        'wp_set_password': r'([\s@;/]*)wp_set_password([\s]*)\(',
        'wp_generate_password': r'([\s@;/]*)wp_generate_password([\s]*)\(',
        'wp_remote_post': r'([\s@;/]*)wp_remote_post([\s]*)\(',
        'wp_remote_get': r'([\s@;/]*)wp_remote_get([\s]*)\(',
        'wp_handle_upload': r'([\s@;/]*)wp_handle_upload([\s]*)\(',

}
sql_injection_regex = {
        'update': r'[\'\"]update(\s+)(.*?)(\s+)set',
        'insert':'insert(\s+)into(\s+)(.*?)(\s+)'
}
def scan_dir(path) -> dict:
    all_df = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            key, value = os.path.basename(subdir), file
            if value.endswith(".php"):
                all_df.setdefault(key, []).append(value)
    return all_df
def scan_zip(path) -> dict:
    all_df = {}
    pyzip = PyZip().from_file(path, inflate=False)
    for key, val in pyzip.zip_content.items():
        if os.path.basename(key).endswith(".php"):
            key, value = os.path.dirname(key), {"filename": os.path.basename(key), "content": val.decode("utf-8")}
            all_df.setdefault(key, []).append(value)
    return all_df