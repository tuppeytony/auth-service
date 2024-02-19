from fastapi import APIRouter


router = APIRouter(tags=['Хелфчек'])


@router.get('/healthcheck')
def healthcheck() -> dict[str, str]:
    """Хелфчек сервиса."""
    return {'status': 'ok'}
