from pandas.core.indexes.accessors import Properties

from src.examples.program.traccar.broadcast.broadcastService import BroadcastService
from src.examples.program.traccar.broadcast.multicastBroadcastService import MulticastBroadcastService
from src.examples.program.traccar.broadcast.nullBroadcastService import NullBroadcastService
from src.examples.program.traccar.config.config import Config
from src.examples.program.traccar.config.keys import Keys
from src.examples.program.traccar.database.ldapProvider import LdapProvider
from src.examples.program.traccar.database.openIdProvider import OpenIdProvider
from src.examples.program.traccar.database.statisticManager import StatisticsManager
from src.examples.program.traccar.forward.eventForwarder import EventForwarder
from src.examples.program.traccar.forward.eventForwarderJson import EventForwarderJson
from src.examples.program.traccar.forward.eventForwarderKafka import EventForwarderKafka
from src.examples.program.traccar.forward.eventForwarderMqtt import EventForwarderMqtt
from src.examples.program.traccar.forward.positionForwarder import PositionForwarder
from src.examples.program.traccar.forward.positionForwarderJson import PositionForwarderJson
from src.examples.program.traccar.forward.positionForwarderUrl import PositionForwarderUrl
from src.examples.program.traccar.forward.positionForwarderRedis import PositionForwarderRedis
from src.examples.program.traccar.forward.positionForwarderKafka import PositionForwarderKafka
from src.examples.program.traccar.geocoder.addressFormat import AddressFormat
from src.examples.program.traccar.geocoder.banGeocoder import BanGeocoder
from src.examples.program.traccar.geocoder.bingMapsGeocoder import BingMapsGeocoder
from src.examples.program.traccar.geocoder.factualGeocoder import FactualGeocoder
from src.examples.program.traccar.geocoder.geoapifyGeocoder import GeoapifyGeocoder
from src.examples.program.traccar.geocoder.geocodeFarmGeocoder import GeocodeFarmGeocoder
from src.examples.program.traccar.geocoder.geocodeXyzGeocoder import GeocodeXyzGeocoder
from src.examples.program.traccar.geocoder.geocoder import Geocoder
from src.examples.program.traccar.geocoder.gisgraphyGeocoder import GisgraphyGeocoder
from src.examples.program.traccar.geocoder.googleGeocoder import GoogleGeocoder
from src.examples.program.traccar.geocoder.hereGeocoder import HereGeocoder
from src.examples.program.traccar.geocoder.locationIqGeocoder import LocationIqGeocoder
from src.examples.program.traccar.geocoder.locationIqGeocoder import LocationIqGeocoder
from src.examples.program.traccar.geocoder.mapQuestGeocoder import MapQuestGeocoder
from src.examples.program.traccar.geocoder.mapTilerGeocoder import MapTilerGeocoder
from src.examples.program.traccar.geocoder.mapboxGeocoder import MapboxGeocoder
from src.examples.program.traccar.geocoder.mapmyIndiaGeocoder import MapmyIndiaGeocoder
from src.examples.program.traccar.geocoder.nominatimGeocoder import NominatimGeocoder
from src.examples.program.traccar.geocoder.openCageGeocoder import OpenCageGeocoder
from src.examples.program.traccar.geocoder.positionStackGeocoder import PositionStackGeocoder
from src.examples.program.traccar.geocoder.testGeocoder import TestGeocoder
from src.examples.program.traccar.geocoder.tomTomGeocoder import TomTomGeocoder
from src.examples.program.traccar.geolocation.geolocationProvider import GeolocationProvider
from src.examples.program.traccar.geolocation.googleGeolocationProvider import GoogleGeolocationProvider
from src.examples.program.traccar.geolocation.mozillaGeolocationProvider import MozillaGeolocationProvider
from src.examples.program.traccar.geolocation.openCellIdGeolocationProvider import OpenCellIdGeolocationProvider
from src.examples.program.traccar.geolocation.unwiredGeolocationProvider import UnwiredGeolocationProvider
from src.examples.program.traccar.handler.geocoderHandler import GeocoderHandler
from src.examples.program.traccar.handler.geocoderHandler import GeocoderHandler
from src.examples.program.traccar.handler.geolocationHandler import GeolocationHandler
from src.examples.program.traccar.handler.speedLimitHandler import SpeedLimitProvider, SpeedLimitHandler
from src.examples.program.traccar.helper.objectMapperContextResolver import ObjectMapperContextResolver
from src.examples.program.traccar.helper.sanitizerModule import SanitizerModule
from src.examples.program.traccar.helper.webHelper import WebHelper
from src.examples.program.traccar.mail.logMailManager import LogMailManager
from src.examples.program.traccar.mail.mailManager import MailManager
from src.examples.program.traccar.mail.smtpMailManager import SmtpMailManager
from src.examples.program.traccar.session.cache.cacheManager import CacheManager
from src.examples.program.traccar.sms.httpSmsClient import HttpSmsClient
from src.examples.program.traccar.sms.smsManager import SmsManager
from src.examples.program.traccar.sms.snsSmsClient import SnsSmsClient
from src.examples.program.traccar.speedlimit.overpassSpeedLimitProvider import OverpassSpeedLimitProvider
from src.examples.program.traccar.speedlimit.speedLimitProvider import SpeedLimitProvider
from src.examples.program.traccar.storage.databaseStorage import DatabaseStorage
from src.examples.program.traccar.storage.memoryStorage import MemoryStorage
from src.examples.program.traccar.storage.storage import Storage
from src.examples.program.traccar.web.webServer import WebServer
from src.examples.program.traccar.api.security.loginService import LoginService


class MainModule():


    def __init__(self, configFile):

        self._configFile = None

        self._configFile = configFile

    def configure(self):
        self.bindConstant().annotatedWith("Names.named(\"configFile\")").to(self._configFile)
        "bind(Config.__class__).asEagerSingleton()"
        "bind(Timer.__class__).to(HashedWheelTimer.__class__).in_(Scopes.SINGLETON)"

    @staticmethod
    def provideStorage(injector, config):
        if config.getBoolean(Keys.DATABASE_MEMORY):
            return injector.getInstance(MemoryStorage.__class__)
        else:
            return injector.getInstance(DatabaseStorage.__class__)

    @staticmethod
    def provideObjectMapper(config):
        objectMapper = "ObjectMapper()"
        if config.getBoolean(Keys.WEB_SANITIZE):
            objectMapper.registerModule(SanitizerModule())
        objectMapper.registerModule("JSR353Module()")
        objectMapper.disable("SerializationFeature.WRITE_DATES_AS_TIMESTAMPS")
        return objectMapper

    @staticmethod
    def provideClient(objectMapperContextResolver):
        return "ClientBuilder.newClient().register(objectMapperContextResolver)"

    @staticmethod
    def provideSmsManager(config, client):
        if config.hasKey(Keys.SMS_HTTP_URL):
            return HttpSmsClient(config, client)
        elif config.hasKey(Keys.SMS_AWS_REGION):
            return SnsSmsClient(config)
        return None

    @staticmethod
    def provideMailManager(config, statisticsManager):
        if config.getBoolean(Keys.MAIL_DEBUG):
            return LogMailManager()
        else:
            return SmtpMailManager(config, statisticsManager)

    @staticmethod
    def provideLdapProvider(config):
        if config.hasKey(Keys.LDAP_URL):
            return LdapProvider(config)
        return None

    @staticmethod
    def provideOpenIDProvider(config, loginService, objectMapper):
        if config.hasKey(Keys.OPENID_CLIENT_ID):
            return OpenIdProvider(config, loginService, "HttpClient.newHttpClient()", objectMapper)
        return None

    @staticmethod
    def provideWebServer(injector, config):
        if config.hasKey(Keys.WEB_PORT):
            return WebServer(injector, config)
        return None


    def provideGeocoder(config, client, statisticsManager):
        if config.getBoolean(Keys.GEOCODER_ENABLE):
            type = config.getString(Keys.GEOCODER_TYPE, "google")
            url = config.getString(Keys.GEOCODER_URL)
            id = config.getString(Keys.GEOCODER_ID)
            key = config.getString(Keys.GEOCODER_KEY)
            language = config.getString(Keys.GEOCODER_LANGUAGE)
            formatString = config.getString(Keys.GEOCODER_FORMAT)
            addressFormat = AddressFormat(formatString) if formatString is not None else AddressFormat()

            cacheSize = config.getInteger(Keys.GEOCODER_CACHE_SIZE)
            geocoder = None
            if type == "test":
                geocoder = TestGeocoder()
            elif type == "nominatim":
                geocoder = NominatimGeocoder(client, url, key, language, cacheSize, addressFormat)
            elif type == "locationiq":
                geocoder = LocationIqGeocoder(client, url, key, language, cacheSize, addressFormat)
            elif type == "gisgraphy":
                geocoder = GisgraphyGeocoder(client, url, cacheSize, addressFormat)
            elif type == "mapquest":
                geocoder = MapQuestGeocoder(client, url, key, cacheSize, addressFormat)
            elif type == "opencage":
                geocoder = OpenCageGeocoder(client, url, key, language, cacheSize, addressFormat)
            elif type == "bingmaps":
                geocoder = BingMapsGeocoder(client, url, key, cacheSize, addressFormat)
            elif type == "factual":
                geocoder = FactualGeocoder(client, url, key, cacheSize, addressFormat)
            elif type == "geocodefarm":
                geocoder = GeocodeFarmGeocoder(client, key, language, cacheSize, addressFormat)
            elif type == "geocodexyz":
                geocoder = GeocodeXyzGeocoder(client, key, cacheSize, addressFormat)
            elif type == "ban":
                geocoder = BanGeocoder(client, cacheSize, addressFormat)
            elif type == "here":
                geocoder = HereGeocoder(client, url, id, key, language, cacheSize, addressFormat)
            elif type == "mapmyindia":
                geocoder = MapmyIndiaGeocoder(client, url, key, cacheSize, addressFormat)
            elif type == "tomtom":
                geocoder = TomTomGeocoder(client, url, key, cacheSize, addressFormat)
            elif type == "positionstack":
                geocoder = PositionStackGeocoder(client, key, cacheSize, addressFormat)
            elif type == "mapbox":
                geocoder = MapboxGeocoder(client, key, cacheSize, addressFormat)
            elif type == "maptiler":
                geocoder = MapTilerGeocoder(client, key, cacheSize, addressFormat)
            elif type == "geoapify":
                geocoder = GeoapifyGeocoder(client, key, language, cacheSize, addressFormat)
            else:
                geocoder = GoogleGeocoder(client, key, language, cacheSize, addressFormat)
            geocoder.setStatisticsManager(statisticsManager)
            return geocoder
        return None


    @staticmethod


    def provideGeolocationProvider(config, client):
        if config.getBoolean(Keys.GEOLOCATION_ENABLE):
            type = config.getString(Keys.GEOLOCATION_TYPE, "mozilla")
            url = config.getString(Keys.GEOLOCATION_URL)
            key = config.getString(Keys.GEOLOCATION_KEY)
            if type == "google":
                return GoogleGeolocationProvider(client, key)
            elif type == "opencellid":
                return OpenCellIdGeolocationProvider(client, url, key)
            elif type == "unwired":
                return UnwiredGeolocationProvider(client, url, key)
            else:
                return MozillaGeolocationProvider(client, key)
        return None


    @staticmethod


    def provideSpeedLimitProvider(config, client):
        if config.getBoolean(Keys.SPEED_LIMIT_ENABLE):
            type = config.getString(Keys.SPEED_LIMIT_TYPE, "overpass")
            url = config.getString(Keys.SPEED_LIMIT_URL)
            return OverpassSpeedLimitProvider(client, url)
        return None


    @staticmethod


    def provideGeolocationHandler(config, geolocationProvider, cacheManager, statisticsManager):
        if geolocationProvider is not None:
            return GeolocationHandler(config, geolocationProvider, cacheManager, statisticsManager)
        return None


    @staticmethod


    def provideGeocoderHandler(config, geocoder, cacheManager):
        if geocoder is not None:
            return GeocoderHandler(config, geocoder, cacheManager)
        return None


    @staticmethod


    def provideSpeedLimitHandler(speedLimitProvider):
        if speedLimitProvider is not None:
            return SpeedLimitHandler(speedLimitProvider)
        return None

    @staticmethod
    def provideEventForwarder(config, client, objectMapper):
        if config.hasKey(Keys.EVENT_FORWARD_URL):
            forwardType = config.getString(Keys.EVENT_FORWARD_TYPE)
            if forwardType == "kafka":
                return EventForwarderKafka(config, objectMapper)
            elif forwardType == "mqtt":
                return EventForwarderMqtt(config, objectMapper)
            else:
                return EventForwarderJson(config, client)
        return None

    @staticmethod


    def providePositionForwarder(config, client, objectMapper):
        if config.hasKey(Keys.FORWARD_URL):
            if config.getString(Keys.FORWARD_TYPE) is "json":
                return PositionForwarderJson(config, client, objectMapper)
            elif config.getString(Keys.FORWARD_TYPE) is "kafka":
                return PositionForwarderKafka(config, objectMapper)
            elif config.getString(Keys.FORWARD_TYPE) is "redis":
                return PositionForwarderRedis(config, objectMapper)
            else:
                return PositionForwarderUrl(config, client, objectMapper)
        return None

    @staticmethod


    def provideVelocityEngine(config):
        properties = Properties()
        properties.setProperty("resource.loader.file.path", config.getString(Keys.TEMPLATES_ROOT) + "/")
        properties.setProperty("web.url", WebHelper.retrieveWebUrl(config))

        velocityEngine = "VelocityEngine()"
        velocityEngine.init(properties)
        return velocityEngine


