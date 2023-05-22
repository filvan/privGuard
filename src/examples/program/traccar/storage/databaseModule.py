import this

from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys

class DatabaseModule():

    @staticmethod
    def provideDataSource(config):

        driverFile = config.getString(Keys.DATABASE_DRIVER_FILE)
        if driverFile is not None:
            classLoader = this.getSystemClassLoader()
            try:
                method = type(classLoader).getDeclaredMethod("addURL", str.__class__)
                method.setAccessible(True)
                #method.invoke(classLoader, (File(driverFile)).toURI().toURL())
            except Exception as e:
                method = type(classLoader).getDeclaredMethod("appendToClassPathForInstrumentation", str.__class__)
                method.setAccessible(True)
                method.invoke(classLoader, driverFile)

        driver = config.getString(Keys.DATABASE_DRIVER)
        if driver is not None:
            __class__.forName(driver)

        hikariConfig = ""#HikariConfig()
        hikariConfig.setDriverClassName(driver)
        hikariConfig.setJdbcUrl(config.getString(Keys.DATABASE_URL))
        hikariConfig.setUsername(config.getString(Keys.DATABASE_USER))
        hikariConfig.setPassword(config.getString(Keys.DATABASE_PASSWORD))
        hikariConfig.setConnectionInitSql(config.getString(Keys.DATABASE_CHECK_CONNECTION))
        hikariConfig.setIdleTimeout(600000)

        maxPoolSize = config.getInteger(Keys.DATABASE_MAX_POOL_SIZE)
        if maxPoolSize != 0:
            hikariConfig.setMaximumPoolSize(maxPoolSize)

        dataSource = ""#ikariDataSource(hikariConfig)

        if config.hasKey(Keys.DATABASE_CHANGELOG):

            resourceAccessor = ""#DirectoryResourceAccessor(File("."))

            database = "DatabaseFactory.getInstance().openDatabase(config.getString(Keys.DATABASE_URL), config.getString(Keys.DATABASE_USER), config.getString(Keys.DATABASE_PASSWORD), config.getString(Keys.DATABASE_DRIVER), None, None, None, resourceAccessor)"

            changelog = config.getString(Keys.DATABASE_CHANGELOG)

            with this.Liquibase(changelog, resourceAccessor, database) as liquibase:
                liquibase.clearCheckSums()
                liquibase.update(this.Contexts())

        return dataSource
