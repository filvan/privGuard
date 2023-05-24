class ExpressionEvaluatorFactory():

    def __init__(self):

        self._permissions = None



    def createExpressionEvaluator(self, expression):
        expressionEvaluator = "JexlExpressionEvaluator()" if expression is None else JexlExpressionEvaluator(expression)
        expressionEvaluator.setJexlEngine(("JexlBuilder()").silent(True).strict(False).permissions(self._permissions).create())
        return expressionEvaluator

    class JexlPermissionsAnonymousInnerClass():
        def allow(self, pack):
            return True

        def allow(self, clazz):
            return True

        def allow(self, ctor):
            return True

        def allow(self, method):
            return True

        def allow(self, field):
            return True

        def compose(self, *src):
            return self
