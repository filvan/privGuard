from tensorflow.compiler.xla.xla_data_pb2 import Format


class AddressFormat(Format):

    def _initialize_instance_fields(self):

        self._format = None



    def __init__(self):
        self("%h %r, %t, %s, %c")

    def __init__(self, format):
        self._initialize_instance_fields()

        self._format = format

    @staticmethod
    def _replace(s, key, value):
        if value is not None:
            s = s.replace(key, value)
        else:
            s = s.replaceAll("[, ]*" + key, "")
        return s

    def format(self, o, stringBuffer, fieldPosition):
        address = o
        result = self._format

        result = AddressFormat._replace(result, "%p", address.getPostcode())
        result = AddressFormat._replace(result, "%c", address.getCountry())
        result = AddressFormat._replace(result, "%s", address.getState())
        result = AddressFormat._replace(result, "%d", address.getDistrict())
        result = AddressFormat._replace(result, "%t", address.getSettlement())
        result = AddressFormat._replace(result, "%u", address.getSuburb())
        result = AddressFormat._replace(result, "%r", address.getStreet())
        result = AddressFormat._replace(result, "%h", address.getHouse())
        result = AddressFormat._replace(result, "%f", address.getFormattedAddress())

        result = result.replaceAll("^[, ]*", "")

        return stringBuffer.append(result)

    def parseObject(self, s, parsePosition):
        raise Exception()
