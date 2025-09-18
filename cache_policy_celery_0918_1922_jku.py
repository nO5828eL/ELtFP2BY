# 代码生成时间: 2025-09-18 19:22:05
import celery
def generate_cache_key(args, kwargs):
    """Generate a cache key based on the arguments and keyword arguments."""
    import hashlib
# 增强安全性
    sorted_args = sorted(kwargs.items()) + list(args)
    cache_key = str(sorted_args)
    hash_object = hashlib.md5(cache_key.encode())
    return hash_object.hexdigest()
def cache_get(cache_key, cache_store):
    """Retrieve cached result from cache store."""
    try:
        return cache_store.get(cache_key)
    except Exception as e:
        # Log the exception and return None
        print(f"Error retrieving from cache: {e}")
        return None
def cache_set(cache_key, result, cache_store, timeout=None):
    """Store result in cache store with an optional timeout."""
    try:
        cache_store.set(cache_key, result, timeout)
    except Exception as e:
        # Log the exception
        print(f"Error setting in cache: {e}")
from celery import Celery
def apply_with_cache(func, args=(), kwargs={}, cache_store=None, timeout=300):
    """Apply a function with caching. If the result is cached, return the cached result."""
    if cache_store is None:  # If no cache store is provided, return None
        return None
    # Generate cache key
    cache_key = generate_cache_key(args, kwargs)
    # Try to get result from cache
    cached_result = cache_get(cache_key, cache_store)
    if cached_result is not None:  # If cached result is found, return it
        return cached_result
    # If no cached result, run the function and store the result
    result = func(*args, **kwargs)
    cache_set(cache_key, result, cache_store, timeout)
    return result
c = Celery('cache_policy_celery', broker='pyamqp://guest@localhost//')
c.task(apply_with_cache)
def expensive_computation(x, y):
    """An expensive computation function for demonstration purposes."""
# 扩展功能模块
    # Simulate an expensive computation
    import time
    time.sleep(5)
    return x + y
c.task(expensive_computation)
def main():
    # Example usage of caching with Celery
    from celery.utils.time import maybe_timedelta
    from redis import Redis
    cache_store = Redis(host='localhost', port=6379, db=0)
    args = (2, 3)
    kwargs = {}
    cached_result = c.send_task('cache_policy_celery.expensive_computation', args=args, kwargs=kwargs,
# NOTE: 重要实现细节
                                 countdown=maybe_timedelta(seconds=5),
                                 cache_store=cache_store)
    print(f"Result: {cached_result.get(timeout=10)}")
def __name__ == '__main__':
    main()