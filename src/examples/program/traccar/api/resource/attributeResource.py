def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    device_id = kwargs.get('extra_args').get('device_id')

    traccar_devices = pd.read_csv(data_folder + "devices/data.csv")
    traccar_devices = traccar_devices[traccar_devices.DeviceId == device_id]
    return traccar_devices