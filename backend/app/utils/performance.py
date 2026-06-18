import asyncio
import functools
import hashlib
import json
import logging
import os
import sqlite3
import threading
import time
from collections import defaultdict
from typing import Any, Callable, Dict, List, Tuple


logger = logging.getLogger("fir_copilot.performance")

_timings: Dict[str, List[float]] = defaultdict(list)
_cache: Dict[Tuple[str, str], Any] = {}
_lock = threading.RLock()
DB_PATH = "data/cache.db"


def init_db():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    namespace TEXT,
                    key TEXT,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (namespace, key)
                )
            """)
            conn.commit()
    except Exception as e:
        logger.error("Failed to initialize SQLite cache: %s", e)


init_db()


def stable_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()


def log_duration(name: str, started_at: float) -> None:
    duration = time.perf_counter() - started_at

    with _lock:
        _timings[name].append(
            duration
        )

    logger.info(
        "agent=%s duration_ms=%.2f",
        name,
        duration * 1000
    )


def timed_agent(name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                started_at = time.perf_counter()

                try:
                    return await func(*args, **kwargs)

                finally:
                    log_duration(
                        name,
                        started_at
                    )

            return async_wrapper

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            started_at = time.perf_counter()

            try:
                return func(*args, **kwargs)

            finally:
                log_duration(
                    name,
                    started_at
                )

        return wrapper

    return decorator


def get_cached(namespace: str, key_data: Any):
    key_hash = stable_hash(key_data)
    key = (namespace, key_hash)

    # Memory check
    with _lock:
        if key in _cache:
            return _cache[key]

    # Database check
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT value FROM cache WHERE namespace = ? AND key = ?",
                (namespace, key_hash)
            )
            row = cursor.fetchone()
            if row:
                value = json.loads(row[0])
                with _lock:
                    _cache[key] = value
                return value
    except Exception as e:
        logger.error("Error reading SQLite cache: %s", e)

    return None


def set_cached(namespace: str, key_data: Any, value: Any):
    key_hash = stable_hash(key_data)
    key = (namespace, key_hash)

    # Store in memory
    with _lock:
        _cache[key] = value

    # Store in database
    try:
        value_json = json.dumps(value)
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (namespace, key, value) VALUES (?, ?, ?)",
                (namespace, key_hash, value_json)
            )
            conn.commit()
    except Exception as e:
        logger.error("Error writing SQLite cache: %s", e)

    return value


def cached_call(namespace: str, key_data: Any, func: Callable, *args, **kwargs):
    cached = get_cached(
        namespace,
        key_data
    )

    if cached is not None:
        logger.info(
            "cache_hit namespace=%s key=%s",
            namespace,
            stable_hash(key_data)[:12]
        )

        return cached

    result = func(*args, **kwargs)
    return set_cached(
        namespace,
        key_data,
        result
    )


def get_slowest_agents(limit: int = 5):
    summary = []

    with _lock:
        timing_items = list(
            _timings.items()
        )

    for name, durations in timing_items:
        if not durations:
            continue

        total = sum(durations)

        summary.append({
            "agent": name,
            "calls": len(durations),
            "total_ms": round(total * 1000, 2),
            "avg_ms": round((total / len(durations)) * 1000, 2),
            "max_ms": round(max(durations) * 1000, 2)
        })

    return sorted(
        summary,
        key=lambda item: item["total_ms"],
        reverse=True
    )[:limit]

