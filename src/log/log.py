from logging import basicConfig, INFO, StreamHandler, Formatter, getLogger, Logger, WARNING

def setup_log() -> Logger:

    basicConfig(
        filename='simulator.log',
        level=INFO,
        format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console = StreamHandler()
    console.setLevel(INFO)
    formatter = Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    getLogger('azure.iot.device.common.mqtt_transport').setLevel(WARNING)
    getLogger('azure.iot.device.iothub.sync_clients').setLevel(WARNING)
    getLogger('azure.iot.device.common.pipeline.pipeline_stages_mqtt').setLevel(WARNING)
    getLogger('azure.iot.device.iothub.abstract_clients').setLevel(WARNING)
    getLogger('').addHandler(console)
    return getLogger(__name__)
