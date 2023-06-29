from src.examples.program.traccar.analyze.columns import include_columns_analizer


def run(data_folder, **kwargs):
    pd = kwargs.get('pandas')
    deviceid = kwargs.get('extra_args').get('deviceid')
    traccar_data = pd.read_csv(data_folder + "devices/data.csv")
    print(deviceid)
    traccar_data = traccar_data[traccar_data.DeviceID == deviceid]
    traccar_data = traccar_data.sort_values(by='LastUpdate')
    extra_args = kwargs.get('extra_args')
    extra_args.__setitem__('clazz','Position')
    extra_args.__setitem__('columns',['PositionID','Latitude', 'Longitude', 'Altitude', 'Address'])
    kwargs.__setitem__('extra_args',extra_args)
    res = include_columns_analizer.run(data_folder, **kwargs)
    return res[res.PositionID == 'int(traccar_data.iloc[-1,0].PositionID)']