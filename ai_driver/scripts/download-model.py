import argparse
import base64
import json
import os
from pathlib import Path
from loguru import logger
import requests
import tqdm
from requests.adapters import HTTPAdapter
from tqdm.contrib.concurrent import thread_map
from concurrent.futures import ThreadPoolExecutor


def download_file(url, output_folder):
    progress_bar = None
    filename = os.path.basename(url)
    output_path = os.path.join(output_folder, filename)
    headers = {}
    mode = "wb"
    logger.info(url)
    try:
        with requests.get(url, stream=True, headers=headers, timeout=10) as r:
            r.raise_for_status()  # Do not continue the download if the request was unsuccessful
            logger.info(r)
            total_size = int(r.headers.get("content-length", 0))
            block_size = 1024 * 1024  # 1MB
            with open(output_path, mode) as f:
                with tqdm.tqdm(
                    total=total_size,
                    unit="iB",
                    unit_scale=True,
                    bar_format="{l_bar}{bar}| {n_fmt:6}/{total_fmt:6} {rate_fmt:6}",
                ) as t:
                    count = 0
                    for data in r.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                        if total_size != 0 and progress_bar is not None:
                            count += len(data)
                            progress_bar(
                                float(count) / float(total_size),
                                f"Downloading {filename}",
                            )

    except Exception as e:
        logger.info(e)


def get_download_links(session, model, branch):
    base = "https://huggingface.co"
    page = f"/api/models/{model}/tree/{branch}"
    cursor = b""

    links = []
    while True:
        url = f"{base}{page}" + (f"?cursor={cursor.decode()}" if cursor else "")
        r = session.get(url, timeout=10)
        r.raise_for_status()
        content = r.content

        dict = json.loads(content)
        if len(dict) == 0:
            break

        for i in range(len(dict)):
            fname = dict[i]["path"]
            if fname in ["1_Pooling", "2_Dense"]:
                logger.info(f"Subdir for sentence embed : {fname}")
                links.append(
                    f"https://huggingface.co/{model}/resolve/{branch}/{fname}/config.json"
                )
                links.append(
                    f"https://huggingface.co/{model}/resolve/{branch}/{fname}/pytorch_model.bin"
                )
                continue
            link = f"https://huggingface.co/{model}/resolve/{branch}/{fname}"
            logger.info(link)
            links.append(link)

        cursor = (
            base64.b64encode(f'{{"file_name":"{dict[-1]["path"]}"}}'.encode()) + b":50"
        )
        cursor = base64.b64encode(cursor)
        cursor = cursor.replace(b"=", b"%3D")
    return links


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # models = ["TheBloke/MPT-7B-Instruct-GGML", "TheBloke/Llama-2-7B-Chat-GGML"]
    sentence_models = ["sentence-transformers/all-MiniLM-L6-v2", "hkunlp/instructor-xl"]
    models = sentence_models
    branch = "main"
    threads = 6
    output_base = "artifacts"
    retries = 5

    for model in models:
        session = requests.Session()

        session.mount(
            "https://cdn-lfs.huggingface.co", HTTPAdapter(max_retries=retries)
        )
        session.mount("https://huggingface.co", HTTPAdapter(max_retries=retries))
        session.headers = {
            "authorization": f'Bearer {os.getenv("HUGGINGFACE_API_TOKEN")}'
        }

        output_folder = f"{'_'.join(model.split('/')[-2:])}"
        output_folder = Path(output_base) / output_folder

        links = get_download_links(session, model, branch)
        output_folder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Downloading from url: https://huggingface.co/{model}")

        # Downloading the files
        print(f"Downloading the model to {output_folder}")
        thread_map(
            lambda url: download_file(url, output_folder),
            links,
            max_workers=threads,
            disable=True,
        )

        # with ThreadPoolExecutor(max_workers=threads) as executor:
        #     futures = []
        #     for url in links:
        #         futures.append(executor.submit(download_file, url, output_folder))
        #     for future in tqdm.tqdm(futures, desc="Downloading files", unit="file"):
        #         future.result()
