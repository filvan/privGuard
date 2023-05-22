from src.analyze import parse


class QueryBuilder:




    def __init__(self, config, dataSource, objectMapper, query, returnGeneratedKeys):

        self._config = None
        self._objectMapper = None
        self._indexMap = {}
        self._connection = None
        self._statement = None
        self._query = None
        self._returnGeneratedKeys = False

        self._config = config
        self._objectMapper = objectMapper
        self._query = query
        self._returnGeneratedKeys = returnGeneratedKeys
        if query is not None:
            self._connection = dataSource.getConnection()
            parsedQuery = parse(query.trim(), self._indexMap)
            try:
                if returnGeneratedKeys:
                    self._statement = self._connection.prepareStatement(parsedQuery, Statement.RETURN_GENERATED_KEYS)
                else:
                    self._statement = self._connection.prepareStatement(parsedQuery)
            except RuntimeError as error:
                self._connection.close()
                raise error
