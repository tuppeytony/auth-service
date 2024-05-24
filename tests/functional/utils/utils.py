from time import sleep

from docker import DockerClient
from docker.models.containers import Container


def wait_until_docker_healthy(container: Container, docker_client: DockerClient, retries: int = 5) -> None:
    """Хелфсчек для контейнеров докера."""
    sleep_time = 2.0
    step = 1.0
    for _ in range(retries):
        inspect_results = docker_client.api.inspect_container(container.name)
        status = inspect_results['State']['Health']['Status']
        if status != 'healthy':
            sleep_time += step
            sleep(sleep_time)
        else:
            break
