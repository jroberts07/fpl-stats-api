import time
import uuid

from sanic.log import logger


def fpl_log_request(method, path, body):
    start_time = time.time()
    uid = str(uuid.uuid4())
    logger.info(
        "uid: {0} | request: [{1}] {2} | body: {3}".format(
            uid, method, path, body
        )
    )
    return start_time, uid


def fpl_log_response(start_time, uid, status, body):
    spend_time = round((time.time() - start_time) * 1000)
    logger.info(
        "uid: {0} | response code: {1} | body: {2} | time: {3}ms".format(
            uid, status, body, spend_time
        )
    )
