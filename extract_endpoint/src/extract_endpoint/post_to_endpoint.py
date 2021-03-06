import os
import hashlib
import secrets
import typing
from http import HTTPStatus
import requests
import click


DEFAULT_ETL_SECRET_KEY = 'no key'

DEFAULT_ENERGUIDE_ENDPOINT_ADDRESS = 'http://127.0.0.1:5000'


def _etl_secret_key() -> str:
    return os.environ.get('ETL_SECRET_KEY', DEFAULT_ETL_SECRET_KEY)


def _endpoint_address() -> str:
    return os.environ.get('ENERGUIDE_ENDPOINT_ADDRESS', DEFAULT_ENERGUIDE_ENDPOINT_ADDRESS)


def post_stream(stream: typing.IO[bytes],
                timestamp: str,
                url: str) -> int:

    data = stream.read()
    salt = secrets.token_hex(16)

    hasher = hashlib.new('sha3_256')
    hasher.update((salt + _etl_secret_key()).encode())
    hasher.update(data)
    signature = hasher.hexdigest()

    try:
        post_return = requests.post(url=url,
                                    files={'file': data},
                                    data={'salt': salt, 'signature': signature, 'timestamp': timestamp})
        return post_return.status_code
    except requests.exceptions.ConnectionError:
        return HTTPStatus.BAD_GATEWAY


def trigger_tl(url) -> int:
    salt = secrets.token_hex(16)
    hasher = hashlib.new('sha3_256')
    hasher.update((salt + _etl_secret_key()).encode())
    signature = hasher.hexdigest()
    data = dict(salt=salt, signature=signature)
    try:
        return requests.post(url, data=data).status_code
    except requests.exceptions.ConnectionError:
        return HTTPStatus.BAD_GATEWAY


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument('stream', type=click.File('rb'))
@click.argument('timestamp')
@click.option('--url', default=_endpoint_address() + '/upload_file')
def upload(stream: typing.IO[bytes], timestamp: str, url: str) -> None:
    return_code = post_stream(stream=stream, timestamp=timestamp, url=url)
    click.echo(f"Response: {return_code}")
    if return_code != HTTPStatus.OK:
        exit(return_code)


@main.command()
@click.option('--url', default=_endpoint_address() + '/run_tl')
def run_tl(url: str) -> None:
    return_code = trigger_tl(url)
    click.echo(f"Response: {return_code}")
    if return_code != HTTPStatus.OK:
        exit(return_code)


@main.command()
@click.option('--url', default=_endpoint_address() + '/status')
def status(url: str) -> None:
    try:
        system_status = requests.get(url).content.decode()
    except requests.exceptions.RequestException:
        system_status = "Endpoint: Error   TL: Unknown"
    click.echo(f"System Status: {system_status}")
