from ai_driver.server.crud.sessions import get_history, get_sessions
from ai_driver.server import schemas
from redis.client import Redis
import pytest
from loguru import logger
from pytest_redis import factories

redis_my_proc = factories.redis_proc(port=56379)
redisdb: Redis = factories.redisdb("redis_my_proc", decode=True)


def test_get_history_new_session(redisdb: Redis):
    result = get_history("new_session_id", "user_id", store=redisdb)
    logger.info(result)
    assert result.history == []
    assert result.session_id == "new_session_id"
    assert result.user_id == "user_id"


def test_get_history_existing_session(redisdb: Redis):
    user_id = "1"
    redisdb.lpush(
        f"session_list:{user_id}", "existing_session_id", "existing_session_id2"
    )

    result = get_history("existing_session_id", "user_id", store=redisdb)
    logger.info(result)
    assert result.history == []
    assert result.session_id == "existing_session_id"
    assert result.user_id == "user_id"


def test_get_history_deserialization_error(redisdb: Redis):
    session_id = "existing_session_id"
    user_id = "user_id"
    redisdb.lpush(f"session_list:{user_id}", session_id)
    redisdb.set(session_id, "invalid_jsoddn1")

    with pytest.raises(Exception, match="Error deserializing chat history"):
        get_history(session_id, user_id, store=redisdb)


def test_should_get_session(redisdb: Redis):
    user_id = "2"
    pipe = redisdb.pipeline()
    for val in ["existing_session_id", "existing_session_id2"]:
        pipe.lpush(f"session_list:{user_id}", val)
        pipe.execute()
    result = get_sessions(user_id, store=redisdb)
    logger.info(result)
    assert result == ["existing_session_id2", "existing_session_id"]
