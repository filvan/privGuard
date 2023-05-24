from src.examples.program.traccar.model.event import Event
from src.examples.program.traccar.model.position import Position

class OverspeedProcessor:

    ATTRIBUTE_SPEED = "speed"

    def __init__(self):
        pass

    @staticmethod
    def updateState(state, position, speedLimit, minimalDuration, geofenceId):

        state.setEvent(None)

        oldState = state.getOverspeedState()
        if oldState:
            newState = position.getSpeed() > speedLimit
            if newState:
                if state.getOverspeedTime() is not None:
                    oldTime = state.getOverspeedTime().getTime()
                    newTime = position.getFixTime().getTime()
                    if newTime - oldTime > minimalDuration:

                        event = Event(Event.TYPE_DEVICE_OVERSPEED, position)
                        event.set(OverspeedProcessor.ATTRIBUTE_SPEED, position.getSpeed())
                        event.set(Position.KEY_SPEED_LIMIT, speedLimit)
                        event.setGeofenceId(state.getOverspeedGeofenceId())

                        state.setOverspeedTime(None)
                        state.setOverspeedGeofenceId(0)
                        state.setEvent(event)

            else:
                state.setOverspeedState(False)
                state.setOverspeedTime(None)
                state.setOverspeedGeofenceId(0)
        elif position is not None and position.getSpeed() > speedLimit:
            state.setOverspeedState(True)
            state.setOverspeedTime(position.getFixTime())
            state.setOverspeedGeofenceId(geofenceId)
