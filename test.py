import logging
import time
from jaeger_client import Config

if __name__ == "__main__":
    log_level = logging.DEBUG
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name='your-app-name',
        validate=True,
    )
    # this call also sets opentracing.tracer
    tracer = config.initialize_tracer()

    with tracer.start_span('ROOT') as span:
        if span:
            span.log_kv({'event': 'test message', 'life': 42})

        with tracer.start_span('CHILD', child_of=span) as child_span:
            if child_span:
                child_span.log_kv({'event': 'down below'})

    with tracer.start_span('ROOT2') as span:
        if span:
            span.log_kv({'event': 'test message', 'life': 42})
    time.sleep(2)   # yield to IOLoop to flush the spans - https://github.com/jaegertracing/jaeger-client-python/issues/50
    tracer.close()  # flush any buffered spans
